# Steerable Lens — Confidence Is Not Evidence

An interactive companion to the Steerable Lens research project.

## Explore

- Nine illustrative MNIST and CelebA comparisons across Pixel, Fourier phase, CSP phase, and Joint CSP, at matched image distance.
- Six reconstruction panels with a warp-only / warp-plus-gain switch.
- Six current-reference natural-image trajectories with twelve saved frames, driver and judge scores, and image distance.
- Evaluation protocol, a small human pilot, limitations, and downloadable figures and data.

This repository contains the website and selected research outputs, not the full experimental code or datasets. Examples are illustrative; selection and common-attainment conditions are stated on the page. Fonts and research assets are self-hosted. Visitor analytics is optional and configured as described below.

## Visitor analytics

`analytics.js` is loaded by the homepage and interactive results page. Its endpoint belongs to the owner's [private GoatCounter dashboard](https://fmahdisoltani.goatcounter.com/). The dashboard requires sign-in and the public visitor-counter feature is disabled. Sessions are enabled to estimate unique visitors; individual-pageview records, referrers, browser/system, screen-size, location and language statistics are disabled.

1. Keep the GoatCounter dashboard private. Do not enable the public dashboard, visitor counter, or individual-pageview collection. Its site domain is `https://fmahdisoltani.github.io`, because recorded paths already include `/steerable-lens/`.
2. If changing accounts, update `endpoint` in `analytics.js` to the new account's `https://YOUR-CODE.goatcounter.com/count` URL. The site code is public; never put an account password or API key in this repository.
3. Deploy and confirm one intentional production page load appears in the private dashboard. That verification pageview counts as a visit. Browser privacy settings and blockers may prevent some visits from being recorded.

The loader runs only on HTTPS `fmahdisoltani.github.io` at the three explicitly allowed project paths. It normalizes `index.html`, sends no query string, hash or referring-page address, records no click events, and respects Do Not Track and Global Privacy Control. Local previews and the local research gallery never contact the analytics provider. Pageviews and estimated visitors are different measures; these statistics begin only after activation and cannot recover historical visits. The page has no visible counter or widget; a small footer Privacy link describes collection.

## Local preview

Serve this directory with a static HTTP server, for example:

```sh
python3 -m http.server 8000
```

Then open http://localhost:8000. Opening the HTML through a file URL will not load the JSON data reliably.

## Editing

- `index.html`: homepage content and gallery records
- `narrative.css`: homepage typography, layout, and responsive contents menu
- `story.js`: active-section navigation and the four-method explainer
- `animations.js`: homepage GIF playback and gallery selectors
- `explore.html`: separate interactive results page
- `styles.css` and `app.js`: interactive results page appearance, charts, and trajectory playback
- `data.json`: recorded values, relative image paths, and source-file hashes
- `assets/`: saved experimental images and two original paper figures

Preserve the selection disclosures, metric definitions, and common-attainment denominators when changing examples. Images were exported from recorded arrays with only float-to-8-bit conversion. The research paper and full research-code links can be added when public URLs are available.

## GitHub Pages

The site is a plain static page. Publish from the root of the `main` branch; `.nojekyll` preserves the assets without Jekyll processing. Changes pushed to `main` update the website through GitHub Pages.

## Current layout and animations

The homepage uses a reading-focused research narrative inspired by Remember to be Curious (https://recuriosity.github.io/): a centered title, opening morph sequence, short explanatory sections, and a fixed contents menu. The contents menu collapses on smaller screens. The four-method explainer is schematic; all experimental GIFs and datasets are retained unchanged. Longer abstract and replay details are available in expandable notes. The earlier interactive page remains at `explore.html`.

GIFs linked from the page display actual optimization sequences, without image interpolation. The main comparison contains 122 animation frames and includes the source, every accepted step before the requested budget, and the exact matched-budget endpoint for all eight trajectories. These trajectories were replayed with the original settings; final pixels and G/O/O2 probabilities match the published endpoints exactly. Shorter trajectories hold recorded states to finish together. `animations.js` provides shared pause/play controls and respects the operating system's reduced-motion preference by showing endpoint posters. Static charts remain static. GIF color quantization is a format limitation; the interactive page displays PNG frames.

The original fonts are self-hosted in `fonts/`; their included OFL licenses apply. No external font service is contacted by the page.

The CelebA gallery contains eight additional cases: two each for adding/removing smiles and eyeglasses. It loads one selected animation at a time and shares the pause/play and reduced-motion controls. The cases are the first two source IDs with common attainment in each direction, excluding Eyeglasses_183143 already in the main comparison. All 32 method replays match the original endpoint pixels and G/O/O2 probabilities exactly. Every recorded state appears; shorter paths hold frames. Frame counts, timing, validation and source checksums are included in `figures/animation_manifest.json`.

The additional natural-image gallery contains the ten supplied sequences: nine legacy cat trajectories and one golf-ball-to-soccer-ball trajectory. Cat GIFs use all twelve exact image panels from the matching saved strips, with the original two-decimal target probabilities. The golf example uses its saved numerical frames and G/O/L2 measurements. Original amplification values are retained and are distinct from the phase caps in the reference examples. The gallery loads one selected GIF at a time and shares the playback/reduced-motion controls. Source hashes, frame geometry and available measurements are recorded in the animation manifest.

All ten additional natural-image examples now include fixed-gradient counterparts and synchronized source/live/fixed comparison GIFs. Fixed computes the gradient once at the source and renders extrapolation steps 0–11; live recomputes after every edit. All original cat panels were exactly reproduced, and the golf live arrays and G/O probabilities reproduced exactly. The first nonzero live/fixed edit is identical in every pair. Amplification, source, target, model and transform settings are equal within each pair; final image distances are not matched. Native fixed step-zero reconstruction error is retained in the numerical records. The original live and separate fixed GIFs remain downloadable.
