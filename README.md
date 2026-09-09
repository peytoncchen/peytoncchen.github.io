# Pey Me Money App Studios

The official website. Static, hosted on GitHub Pages.

- `index.html` — the site (a Claude Design `.dc.html` page, rendered client-side by `support.js`)
- `support.js`, `image-slot.js` — runtime; do not edit by hand
- `assets/` — app screenshots referenced by the `<image-slot src=...>` tags in `index.html`
- `design/` — earlier design versions

## Local preview

```sh
python3 -m http.server 8000
# open http://localhost:8000
```

## Refreshing screenshots

Each `<image-slot>` in `index.html` has a `src` pointing into `assets/`. Replace the file (keep the name) or point `src` at a new one. Phone shots are resized to 900 px tall, wide shots to 1800 px, with `sips -Z`. Sources: SpeedStream, Glovebox and plop from the iOS simulator (each repo's `docs/TESTFLIGHT-AGENT.md` or `docs/testing-and-device-loop.md` lists the launch flags for demo data); ConeCanvas from the Mac editor; Altrove from `docs/verification/screenshots`; AC Autocross Maker from a matplotlib render of `course.json`.
