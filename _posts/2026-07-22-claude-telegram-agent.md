---
title: A Claude agent that lives on Telegram
---

I have been running a Claude Code agent on a small VPS for the past few
weeks. I talk to it through Telegram, like a contact in my phone. It reads
and writes a git repo of plain markdown files, and that repo is its whole
memory. Nothing lives in the chat history. Nothing lives in a database.

## Why

Chat apps forget. Close the window, and the model starts from zero next
time. I wanted something that keeps state across restarts, crashes, and
context limits, and that I could inspect and edit by hand if I ever
disagreed with what it remembered.

The design borrows directly from Andrej Karpathy's
[LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
His point: don't make the model re-read raw sources and re-derive the same
facts on every query. Instead, have it read once, write what it learned
into a small set of markdown pages, and treat those pages as the real
memory. The context window is scratch space. The files are the truth.

## How it works

The repo has a few folders:

- `wiki/` — durable facts, one topic per file. Job, training plans, people,
  recipes, whatever is worth knowing next month.
- `journal/` — a dated log, append-only, one entry per day.
- `tasks/` — whatever is in progress right now.

A `CLAUDE.md` file at the root sets the rules: read the wiki index first,
keep pages short, commit and push after every change, ask before anything
destructive. The agent runs as
`claude --channels plugin:telegram@claude-plugins-official --remote-control`,
which handles reconnecting after a restart without losing its place —
a fresh session just reads the files and picks up where the last one left
off.

## Early use

So far it has:

- kept a running log of a 12-week triathlon base block, week by week
- built and tracked a marathon training plan for someone else
- run a periodic "wiki health check" that trims bloated pages and flags
  contradictions before they pile up
- held a reading list and a small stack of recipes
- written this post

None of it is exotic. The point was never a clever demo — it was an agent
that still knows what it knew last week.
