# Profile rendering performance

The profile keeps the Medusa's liquid motion, both silver mathematical figures,
the icon sheen, responsive layouts and reduced-motion versions. The published
animated header is now pre-rendered WebP. The earlier sections below document
the retained SVG source and the company-logo optimizations; the final section
describes the current header and its tradeoffs.

## Changes

- The animated desktop header is **125,600 bytes**, down from **322,856 bytes**
  at `4c64e7f` (61.1% smaller, before transfer compression).
- The portrait is 332 × 332 WebP, covering twice its 166 × 166 display dimensions.
  Its file is 31,782 bytes instead of 87,278. The original artwork is retained.
- Each mathematical strand uses 12 tangent-matched cubic Bezier segments rather
  than 128 straight segments. Phase, frequency, loop timing and line style remain
  the same. Coordinates are rounded below the visible pixel scale.
- Static labels, original icon paths and the outlined signature are embedded as
  one static SVG image layer. The browser can reuse this resource while drawing
  the moving layers. Text stays vector, and the outer image retains its accessible
  description. No browser script, external service or rasterized text is added.
- Goo filtering is bounded to the avatar's visible 360 × 360 region. A second
  blurred copy of the animated mask is replaced by inexpensive radial shadow
  gradients following the droplets. The actual blur/threshold fusion remains.
- Header filenames continue to include a content hash, preventing stale images
  from being reused after a rebuild.

## Measurement

Chromium headless, 1120 × 700 viewport, device scale 1, SVG embedded through an
`img` at 850 px width. CPU throttling was set to 4× using the Chrome DevTools
Protocol. Two alternating five-second runs of the previous and final SVGs were
recorded with `devtools.timeline` tracing after the image decoded.

| Trace event | Before, combined duration/count | After, combined duration/count | Time per event |
| --- | ---: | ---: | ---: |
| Paint | 1237.595 ms / 1092 | 1047.277 ms / 1134 | 18.5% lower |
| Layout | 215.128 ms / 545 | 171.370 ms / 567 | 23.4% lower |

Normalizing by event count matters: the improved version completed more paint
cycles in the same capture window. These are local rendering measurements,
not an FPS guarantee for every device or a measurement of GitHub's surrounding
page. Initial cold runs varied more, so the table uses the repeated runs.

Validation includes all eight header variants, matching content hashes, static
versions without animation, decoding the static vector layer, seamless motion
loops, repeatable rebuilds, and browser checks on desktop/mobile in both themes.

Rebuild using the commands in [profile-layout.md](profile-layout.md).

## Company-logo refresh

The first Prometheus animation put the six moving dots in the same SVG image
document as both company descriptions. Profiling the image showed layout and
paint work continuing throughout that entire composition. The fixed lettering
and Shredeo mark now live in a reusable embedded static SVG layer; the original
seven Prometheus circles remain a separate vector layer above it. No extra
network request or browser script is added.

The 950 ms simultaneous opening remains smooth. Only the subsequent 24-second
rotation uses 720 evenly spaced steps: 30 updates per second, about 0.16 pixels
of motion per step at the original logo size. Reduced-motion variants remain
completely static. Company filenames now include content hashes so README
visitors receive the corrected image rather than a cached earlier version.

The full profile was compared before and after, including the unchanged animated
Medusa and both mathematical figures: Chromium headless, 1120 × 1000 viewport,
850 px article, 4× CPU throttling, HTTP cache disabled. Four local refreshes in
the order before/after/after/before captured navigation, image decoding and
3.5 seconds of frame sampling after DOMContentLoaded.

| Trace event | Before, combined duration/count | After, combined duration/count | Time per event |
| --- | ---: | ---: | ---: |
| Paint | 1659.423 ms / 836 | 1217.420 ms / 826 | 25.7% lower |
| Layout | 256.788 ms / 778 | 182.308 ms / 660 | 16.3% lower |

No sampled animation-frame interval exceeded 25 ms in either optimized run.
These are local, CPU-throttled rendering measurements, not a guarantee about
GitHub network latency or every browser/device. The test harness and raw logs
are local artifacts under `output/playwright/refresh-performance/`.

## Pre-rendered header

`scripts/prerender_header.py` captures the original SVG artwork offline in
Chromium, then encodes it with FFmpeg/libwebp. The four published animated
headers contain 384 frames at 24 fps, with an approximately 16-second infinite
loop. All source motions share that period to avoid a discontinuity at the
boundary. The original SVGs, geometry, portrait and monochrome colors remain
in the repository. Explicit reduced-motion sources remain static SVG images.
Prometheus and company text retain their small SVG composition.

The high-density captures are encoded at 1152 × 444 for desktop and 600 × 1035
for mobile, quality 88. This is lossy image compression: text remains readable
at the profile's display size, but does not have the unlimited scale of the SVG.
The whole-header lossless prototype was rejected at 4,983,012 bytes. A prototype
embedding moving WebP tiles within an otherwise vector SVG animated in Chromium
but remained frozen in Firefox, so it was also rejected.

| Published variant | Bytes |
| --- | ---: |
| Desktop dark | 1,819,580 |
| Desktop light | 1,473,490 |
| Mobile dark | 1,710,194 |
| Mobile light | 1,358,640 |

Only one responsive/theme variant is loaded. These images are substantially
larger than the 125,600-byte desktop SVG source. They trade initial network
transfer and decoded-image memory for eliminating the header's live SVG filters,
path morphing and animation-driven layout. Filenames include a content hash.

The complete profile, including the unchanged animated company composition,
was measured before/after/after/before in Chromium headless: 1120 × 1000,
850 px article, 4× CPU throttling, HTTP cache disabled, navigation plus 3.5 seconds
of frame sampling after DOMContentLoaded in each run.

| Trace event | SVG, combined duration/count | WebP, combined duration/count |
| --- | ---: | ---: |
| Paint | 1141.931 ms / 830 | 461.235 ms / 520 |
| Layout | 210.912 ms / 675 | 53.269 ms / 267 |
| UpdateLayoutTree | 479.510 ms / 820 | 190.679 ms / 412 |
| Decode Image | not recorded separately | 681.254 ms / 171 |

The captured windows show about 60% less paint duration and 75% less layout
duration. Image decoding still costs CPU; this is not a claim of zero CPU or
guaranteed GPU decoding. Neither version missed a sampled 25 ms frame interval
in this final local comparison, so this does not establish a universal FPS gain.
First-visit network conditions and a visitor's browser/device remain relevant.

Validation covers Chromium and Firefox playback in all eight combinations of
desktop/mobile, light/dark and animated/reduced-motion, image dimensions,
384-frame/15,999 ms WebP containers, loop boundaries, and source publication
integrity. Rebuild instructions are in [profile-layout.md](profile-layout.md).
