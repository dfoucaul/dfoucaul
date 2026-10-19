# Profile rendering performance

The profile keeps the Medusa's liquid motion, both silver mathematical figures,
the icon sheen, responsive layouts and reduced-motion versions.

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
