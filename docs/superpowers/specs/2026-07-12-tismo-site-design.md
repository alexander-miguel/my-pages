# tismo — site design

Date: 2026-07-12. Status: approved.

## Purpose

An anonymous personal landing site ("tismo") on GitHub Pages at
`https://alexander-miguel.github.io/my-pages/`. Content is markdown shared
from Obsidian (standard links, no wikilinks) plus standalone HTML+CSS pages.
No personally identifying information anywhere on the site.

## Approach

Jekyll 4 with hand-rolled layouts and a single small CSS file — no theme.
Design language modelled on stephango.com/vault: ~40em measure, light
background, near-black text, muted grey metadata, minimal underlined links,
no JavaScript.

## Structure

- `index.md` — landing page: about-this-site plus links to sections.
- `_posts/` + `blog/index.html` — dated blog posts with an auto-generated
  listing, newest first.
- `_training_plans/` (collection, `output: true`) + `training-plans/index.html`
  — training plan pages with an auto-generated listing.
- `adhoc/` — escape hatch for standalone HTML+CSS. Files without front matter
  are served verbatim; `adhoc/index.html` auto-lists both static files and
  front-mattered pages in the directory.
- `_layouts/default|page|post.html`, `assets/css/style.css` — the whole design.

## Deployment

`.github/workflows/pages.yml`: on push to `main`, build with Jekyll
(Ruby 3.3, `bundle install`, `jekyll build` with the base path from
`actions/configure-pages`) and deploy via `actions/upload-pages-artifact` +
`actions/deploy-pages`. Repo Pages source is set to "GitHub Actions".

## Decisions

- Obsidian notes arrive with standard markdown links — no wikilink handling.
- Sections + dated blog (collections/_posts), not flat pages.
- `docs/` is excluded from the site build.
- No Gemfile.lock committed initially (no local Ruby new enough to generate
  one); CI runs a plain `bundle install`.
