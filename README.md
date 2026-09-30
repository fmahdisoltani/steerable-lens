# Steerable Lens — Confidence Is Not Evidence

An interactive companion to the Steerable Lens research project.

## Explore

- Nine illustrative MNIST and CelebA comparisons across Pixel, Fourier phase, CSP phase, and Joint CSP, at matched image distance.
- Six reconstruction panels with a warp-only / warp-plus-gain switch.
- Six current-reference natural-image trajectories with twelve saved frames, driver and judge scores, and image distance.
- Evaluation protocol, a small human pilot, limitations, and downloadable figures and data.

This repository contains the website and selected research outputs, not the full experimental code or datasets. Examples are illustrative; selection and common-attainment conditions are stated on the page. The page adds no analytics, tracking scripts, external fonts, or third-party dependencies.

## Local preview

Serve this directory with a static HTTP server, for example:

```sh
python3 -m http.server 8000
```

Then open http://localhost:8000. Opening the HTML through a file URL will not load the JSON data reliably.

## Editing

- `index.html`: page content
- `styles.css`: layout and appearance
- `app.js`: comparisons, charts, and trajectory playback
- `data.json`: recorded values, relative image paths, and source-file hashes
- `assets/`: saved experimental images and two original paper figures

Preserve the selection disclosures, metric definitions, and common-attainment denominators when changing examples. Images were exported from recorded arrays with only float-to-8-bit conversion. The research paper and full research-code links can be added when public URLs are available.

## GitHub Pages

The site is a plain static page. Publish from the root of the `main` branch; `.nojekyll` preserves the assets without Jekyll processing. Changes pushed to `main` update the website through GitHub Pages.
