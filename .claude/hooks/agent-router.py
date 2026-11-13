#!/usr/bin/env python3
"""agent-router (escalation system): automatic escalation when an agent fails.

Ladder for a Sonnet agent:  1 Sonnet high (as pinned) -> 2 Sonnet xhigh (twin) -> 3 Opus -> 4 main session does it.
Ladder for an Opus agent:   1 Opus high (as pinned)   -> 2 Opus xhigh (twin)   -> 3 main session does it.
Only the failed part is redone. One agent at a time unless KIT_PARALLEL=1 (the owner asked for speed).
Never above xhigh, never a model other than Sonnet or Opus, unless KIT_ALLOW_ABOVE=1 (the owner asked).

Wired in .claude/settings.json for PreToolUse, PostToolUse and PostToolUseFailure on the Agent/Task tool.
State: .claude/state/agent-router.json. Log: .claude/state/agent-router.log (one line per decision).
"""
import json, os, re, sys, time
from pathlib import Path

TWIN = "-xhigh"
STATUS_ASK = ("\n\n[agent-router] When you finish, end your reply with exactly one line: "
              "`STATUS: DONE` or `STATUS: FAILED: <the one part that failed>`.")
EXPIRE = 3 * 3600


def root(ev):
    return Path(os.environ.get("CLAUDE_PROJECT_DIR") or ev.get("cwd") or ".")


def state_path(ev):
    p = root(ev) / ".claude" / "state"
    p.mkdir(parents=True, exist_ok=True)
    return p / "agent-router.json"


def load(ev):
    try:
        s = json.loads(state_path(ev).read_text())
    except Exception:
        s = {}
    now = time.time()
    return {k: v for k, v in s.items() if now - v.get("ts", 0) < EXPIRE}


def save(ev, s):
    state_path(ev).write_text(json.dumps(s, indent=1))


def log(ev, msg):
    with open(state_path(ev).parent / "agent-router.log", "a") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + msg + "\n")


def base(name):
    return name[:-len(TWIN)] if name and name.endswith(TWIN) else name


def pinned_model(ev, name):
    for d in (root(ev) / ".claude" / "agents", Path.home() / ".claude" / "agents"):
        p = d / f"{name}.md"
        if p.exists():
            m = re.search(r"^model:\s*(\S+)", p.read_text(encoding="utf-8"), re.M)
            return m.group(1).strip("'\"") if m else None
    return None


def ladder(model):
    # returns list of steps after attempt 1: ("twin"|"opus"|"main")
    return ["twin", "opus", "main"] if model == "sonnet" else ["twin", "main"]


def out(obj):
    print(json.dumps(obj))
    sys.exit(0)


def pre(ev):
    ti = dict(ev.get("tool_input") or {})
    name = ti.get("subagent_type")
    if not name:
        sys.exit(0)
    agent = base(name)
    # caps
    if os.environ.get("KIT_ALLOW_ABOVE") != "1":
        if ti.get("model") and ti["model"] not in ("sonnet", "opus"):
            out({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                 "permissionDecisionReason": f"agent-router: model {ti['model']!r} is above the cap. Only Sonnet or Opus, unless the owner asks."}})
        if ti.get("effort") == "max":
            out({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                 "permissionDecisionReason": "agent-router: effort max is above the cap (xhigh is the ceiling) unless the owner asks."}})
    # one agent at a time
    if os.environ.get("KIT_PARALLEL") != "1" and ti.get("run_in_background") is True:
        ti["run_in_background"] = False
    s = load(ev)
    st = s.get(agent)
    changed = []
    if st and st.get("attempt", 1) > 1:
        step = st["next"]
        if step == "main":
            log(ev, f"{agent}: DENY attempt {st['attempt']} -> main session does it")
            out({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                 "permissionDecisionReason": (f"agent-router: {agent} has failed {st['attempt']-1} times on: {st.get('part')}. "
                                              "Step 4: the MAIN SESSION must do this part itself now. Do only that part, not the whole job. "
                                              f"(Reset: delete the '{agent}' entry in .claude/state/agent-router.json.)")}})
        if step == "twin" and pinned_model(ev, agent + TWIN):
            ti["subagent_type"] = agent + TWIN
            changed.append(f"subagent_type={agent + TWIN} (xhigh)")
        elif step == "opus":
            ti["subagent_type"] = agent
            ti["model"] = "opus"
            changed.append("model=opus")
        prefix = (f"[agent-router] RETRY attempt {st['attempt']}. The earlier run failed on: {st.get('part')}. "
                  "Do ONLY that failed part. Everything else is already done: do not redo it.\n\n")
        ti["prompt"] = prefix + ti.get("prompt", "")
    if STATUS_ASK.strip() not in ti.get("prompt", ""):
        ti["prompt"] = ti.get("prompt", "") + STATUS_ASK
    log(ev, f"{agent}: dispatch attempt {(st or {}).get('attempt', 1)} {' '.join(changed)}")
    out({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow",
         "permissionDecisionReason": "agent-router", "updatedInput": ti}})


def text_of(resp):
    """Collect every string inside the tool response (dicts/lists), joined with newlines."""
    out = []
    def walk(x):
        if isinstance(x, str):
            out.append(x)
        elif isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(resp)
    return "\n".join(out)


def post(ev, failed_tool=False):
    ti = ev.get("tool_input") or {}
    name = ti.get("subagent_type")
    if not name:
        sys.exit(0)
    agent = base(name)
    txt = text_of(ev.get("tool_response")) if not failed_tool else (ev.get("error") or "tool error")
    m = re.search(r"STATUS:\s*FAILED:?\s*(.*)", txt)
    resp = ev.get("tool_response")
    is_err = isinstance(resp, dict) and resp.get("is_error") is True
    failed = failed_tool or bool(m) or is_err
    s = load(ev)
    if not failed:
        if agent in s:
            log(ev, f"{agent}: DONE after attempt {s[agent]['attempt']} -> reset")
            s.pop(agent)
            save(ev, s)
        sys.exit(0)
    part = (m.group(1).strip().splitlines()[0][:300] if m and m.group(1).strip() else txt.strip()[:300]) or "unspecified part"
    st = s.get(agent) or {"attempt": 1, "model": pinned_model(ev, agent) or "sonnet"}
    steps = ladder(st["model"])
    idx = st["attempt"] - 1          # 0 after first failure
    nxt = steps[min(idx, len(steps) - 1)]
    st.update({"attempt": st["attempt"] + 1, "next": nxt, "part": part, "ts": time.time()})
    s[agent] = st
    save(ev, s)
    what = {"twin": f"{agent} again at xhigh effort (the router switches to {agent}{TWIN})",
            "opus": f"{agent} again on Opus (the router sets model=opus)",
            "main": "nobody: the main session must do this part itself"}[nxt]
    log(ev, f"{agent}: FAILED attempt {st['attempt']-1} on '{part}' -> next: {nxt}")
    reason = (f"agent-router: {agent} FAILED (attempt {st['attempt']-1}) on: {part}\n"
              f"Next step: call {what}. Brief it with ONLY the failed part; do not redo the whole job."
              if nxt != "main" else
              f"agent-router: {agent} FAILED (attempt {st['attempt']-1}) on: {part}\n"
              "Next step: the MAIN SESSION does only this failed part itself. Do not call the agent again for it.")
    out({"decision": "block", "reason": reason})


def main():
    ev = json.load(sys.stdin)
    if ev.get("tool_name") not in ("Agent", "Task"):
        sys.exit(0)
    e = ev.get("hook_event_name")
    if e == "PreToolUse":
        pre(ev)
    elif e == "PostToolUse":
        post(ev)
    elif e == "PostToolUseFailure":
        post(ev, failed_tool=True)


if __name__ == "__main__":
    main()
