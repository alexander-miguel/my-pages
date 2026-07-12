# tismo

Source for [tismo](https://alexander-miguel.github.io/my-pages/), a minimal
Jekyll site published to GitHub Pages.

## Publishing

Every push to `main` builds and deploys the site via
`.github/workflows/pages.yml`. Nothing else to do.

## Adding content

- **Blog post** — add `_posts/YYYY-MM-DD-slug.md` with front matter:

  ```yaml
  ---
  title: Post title
  ---
  ```

- **Training plan** — add `_training_plans/name.md` with a `title`. It
  appears on `/training-plans/` automatically.

- **Adhoc HTML page** — drop any standalone `.html` file into `adhoc/`.
  Files without front matter are served exactly as written and listed on
  `/adhoc/` automatically.

- **Obsidian notes** — export/copy with standard markdown links (not
  `[[wikilinks]]`). A note can become a post or a training plan; add the
  front matter above.

## Local preview (optional)

Requires Ruby ≥ 3.1 (e.g. `brew install ruby`), then:

```sh
bundle install
bundle exec jekyll serve
```

Site serves at `http://localhost:4000/my-pages/`.
