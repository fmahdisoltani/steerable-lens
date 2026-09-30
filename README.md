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

## Current layout and animations

The homepage follows the supplied scholarly project-page design. The earlier interactive page remains at `explore.html`.

Twenty-one GIFs used by the page display actual optimization sequences, without image interpolation. The main comparison contains 122 animation frames and includes the source, every accepted step before the requested budget, and the exact matched-budget endpoint for all eight trajectories. These trajectories were replayed with the original settings; final pixels and G/O/O2 probabilities match the published endpoints exactly. Shorter trajectories hold recorded states to finish together. `animations.js` provides shared pause/play controls and respects the operating system's reduced-motion preference by showing endpoint posters. Static charts remain static. GIF color quantization is a format limitation; the interactive page displays PNG frames.

The original fonts are self-hosted in `fonts/`; their included OFL licenses apply. No external font service is contacted by the page.

The CelebA gallery contains eight additional cases: two each for adding/removing smiles and eyeglasses. It loads one selected animation at a time and shares the pause/play and reduced-motion controls. The cases are the first two source IDs with common attainment in each direction, excluding Eyeglasses_183143 already in the main comparison. All 32 method replays match the original endpoint pixels and G/O/O2 probabilities exactly. Every recorded state appears; shorter paths hold frames. Frame counts, timing, validation and source checksums are included in `figures/animation_manifest.json`.

The additional natural-image gallery contains the ten supplied sequences: nine legacy cat trajectories and one golf-ball-to-soccer-ball trajectory. Cat GIFs use all twelve exact image panels from the matching saved strips, with the original two-decimal target probabilities. The golf example uses its saved numerical frames and G/O/L2 measurements. Original amplification values are retained and are distinct from the phase caps in the reference examples. The gallery loads one selected GIF at a time and shares the playback/reduced-motion controls. Source hashes, frame geometry and available measurements are recorded in the animation manifest.
