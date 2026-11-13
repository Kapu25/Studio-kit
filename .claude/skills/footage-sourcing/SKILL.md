---
name: footage-sourcing
---

> **OWNER OVERRIDE (beats anything below):** Only licensed or public-domain material (Wikimedia Commons, Internet Archive public domain, Pexels/Pixabay/Mixkit with the licence noted) and the owner's own AI-made clips (Flow, Meta AI). NEVER pull footage, audio or images from YouTube, Instagram, TikTok or any social platform, with any tool. Every shot and track goes in sources.json with its source URL and licence.

# Footage sourcing

The rule from `film-taste`: real before generated, specific before generic, mixed sources, no stock look. This skill is where the footage comes from and how to keep a clean record of it.

## Where real footage lives

- **Real interviews, news and talks,** cut short and used for commentary. Check what your platform and your country allow, and credit the source.
- **Film shot on real film.** Search free libraries for "super 8", "8mm", "16mm", then pull the whole portfolio of a creator whose scans work. Their scans include the film gate (black borders, sprocket holes): crop inside it (cutfilm take `box: "auto"`).
- **Public domain archive film.** Internet Archive, Prelinger collection: search `https://archive.org/advancedsearch.php` with `collection:(prelinger) AND licenseurl:(*publicdomain*)` plus subjects, list files with `/metadata/<identifier>`, take the h.264 `.mp4`. Some items carry a copyright line on the title card even when marked public domain; check before paid use. Skip title and end cards.
- **Wikimedia Commons.** The best source of real microscopy and many public domain government films. Search with `filemime:video <words>`. `scripts/commons_get.py name="File:..."` downloads stills with licence, author and credit recorded. Commons throttles anonymous agents: send a User-Agent naming the project (never a personal email) and pace requests.
- **NASA and other government agencies:** public domain. Crop out rack labels and mission marks.
- **Headlines and web pages:** capture the real page with headless Chrome (a throwaway `--user-data-dir` per capture, never a personal browser profile), or a Wayback Machine capture (`web.archive.org/web/<year>if_/<url>`) for paywalled pages.
- **Stock libraries (Pexels, Mixkit, Coverr):** last resort for people, fine for nature and textures. Reject posed shots on sight. Probe every file: some labelled 1080p are 720p. Some "free" clips are AI generated or carry restricted licences; check each item's page.

## Fetching

- **Apify** (connect it first; it costs money, so set a spending cap per run):
  - an Instagram reel scraper on a brand's official account for its own vertical footage;
  - a Pexels scraper for keyless search across a creator's portfolio.
  Read long signed URLs from the saved result file in a script, so they never fill the conversation.
- **Decode check everything.** Accept a file only when its size matches and `ffmpeg -v error -i f -f null -` prints nothing. When a segment fetch comes back corrupt, download the whole file and cut it locally. Never trust a resumed download without that check.

## Licences

- **Free to use, no credit:** public domain, CC0, Pexels, Mixkit free licence (check each item: some Mixkit video is restricted to personal use), NASA.
- **CC BY:** fine, but the credit must travel with the post (caption, first comment, or a linked page): title, author, source, licence, and "cropped, retimed and colour graded, with graphics added".
- **CC BY-SA:** skip for anything commercial; share alike could reach the whole film.
- **Third party news, interviews and trailers:** short, transformed, for commentary. This is a judgement about your platform and jurisdiction, not legal advice.

## The provenance record

Every project keeps `sources.json`: per shot, the film time, the file, the source page, the creator, the licence and the credit line. Build `credits.md` from it at delivery. Never state a source from memory; trace it.

## Before a shot goes in

- It decodes clean and is at least HD (or windowed if it is archive SD).
- No watermark, burned in caption, handle, laurel card or third party logo in the frame you will use. Look at the final frames, not just the source strip.
- It is specific to the story, not generic office b roll.
- It does not repeat a camera setup already in the film.
