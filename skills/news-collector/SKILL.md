---
name: news-collector
description: >
  Proactively gather, organize, and present news from RSS feeds as a structured
  dashboard. Trigger on requests for "news", "RSS feed", "daily briefing",
  "current events", "latest headlines", "news summary", "feed reader",
  "keep me updated", "what's new in", "monitor these topics", "show me news about",
  "pull my news digest", "aggregat*", "stay informed on", or when the user asks to
  collect, monitor, or stay updated on topics via RSS. Also trigger if the user asks
  to refresh their news feed or view their configured news sources.
---

# News collector

Use the bundled standard-library script with feed URLs supplied by the caller. It
does not install packages, store preferences, discover feeds, or generate summaries.

```bash
python3 /path/to/skills/news-collector/scripts/rss_reader.py \
  [--timeout SECONDS] https://example.com/feed.xml [https://another.example/rss]
```

# Workflow Overview

Follow these 6 steps in order:

1. Check for existing preferences at `~/.news-collector/preferences.json`
2. If absent/empty/malformed -> **PAUSE** and prompt user for topics/sources
3. (Optional) Web-research fallback if user provides only topics without URLs -> **PAUSE** after presenting discovered feeds
4. Save or update preferences as JSON at `~/.news-collector/preferences.json`
5. Fetch feeds using `scripts/rss_reader.py`
6. Process results, return to user

Steps 2 and 3 are PAUSE checkpoints: the agent must stop and wait for explicit user input before continuing.

# Step-by-step Instructions

## Step 1: Check preferences file

**Path**: `~/.news-collector/preferences.json`

Read the file if it exists. Check if it contains valid JSON with a `"sources"` key that is a non-empty list.

- **If existing preferences are found**: Load them into memory and proceed to Step 5 (fetch feeds). Briefly show the user their current sources/topics: "Your configured sources: [list of source names from prefs]".
- **If no preferences exist** (file not found), or the file is empty, or parsing fails (malformed JSON): proceed to Step 2 (prompt user for new preferences).

## Step 2: Prompt for topics and/or source URLs

**PAUSE checkpoint**: Stop here. Ask the user what topics they are interested in and whether they have specific RSS feed URLs they want to follow.

Accept one of three inputs:
- **Topics only** (e.g., "Technology", "Climate science") -> proceed to Step 3 (web-research fallback)
- **Topics AND feed URLs** (e.g., "Technology -- https://techcrunch.com/feed/") -> skip directly to Step 4 (save preferences)
- **Only feed URLs with no topics** -> assign a topic alias like "Uncategorized" per source, then proceed to Step 4

## Step 3: Web-research fallback (optional)

**Trigger**: This step runs only if the user has provided topics but no URLs, or explicitly says "I don't know any feeds."

**PAUSE checkpoint**: After discovering and presenting URLs to the user, stop. Wait for confirmation before saving anything.

1. Use `webfetch` to search for well-known RSS feed URLs from reputable publishers.
2. Example search queries:
   - `"Reuters Technology RSS feed URL"`
   - `"BBC World Service RSS feed"`
   - `"Associated Press technology news RSS"`
3. Preferred domains (prioritize these when searching):
   - `reuters.com`, `bbc.co.uk`, `apnews.com`, `npr.org`, `wiley.com`, `nature.com`
4. After discovering URLs:
   - Present discovered URLs to the user for confirmation, grouped by topic. Example format:
     ```
     I found these feeds for Technology:
     - Reuters: https://www.reutersagency.com/feed/
     - TechCrunch: https://techcrunch.com/feed/
     ```
   - **Only save URLs the user confirms**. Do not auto-save unconfirmed URLs.

## Step 4: Save preferences

**Path**: `~/.news-collector/preferences.json`

Write preferences to the JSON file using `json.dump()` or the agent's native file-write capability. Follow these rules:

- If an existing file exists, **MERGE** new sources/topics into existing data -- do NOT overwrite unspecified keys (preserve any topics/sources not mentioned by the user).
- Create the parent directory `~/.news-collector/` if it does not exist (`os.makedirs` with `exist_ok=True`).
- Always update `"last_updated"` to the current ISO-8601 UTC timestamp.

