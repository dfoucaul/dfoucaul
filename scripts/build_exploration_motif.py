"""Original phase-shifting Lissajous curves, rendered as a self-contained SVG."""

from math import cos, pi, sin
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEGMENTS = 12
STEPS = 16


def curve(phase, strand, variant="exploration"):
    frequency_x, frequency_y = (2, 3) if variant == "building" else (3, 2)

    def point(t):
        return (50 + 39 * sin(frequency_x * t + phase + strand * .11),
                32 + 25 * sin(frequency_y * t + strand * .08))

    def tangent(t):
        return (39 * frequency_x * cos(frequency_x * t + phase + strand * .11),
                25 * frequency_y * cos(frequency_y * t + strand * .08))

    # Hermite-to-Bezier interpolation preserves the sine's tangents with 12
    # cubic segments, instead of interpolating 128 independent vertices/frame.
    step = 2 * pi / SEGMENTS
    x, y = point(0)
    commands = [f"M{x:.1f},{y:.1f}"]
    for index in range(SEGMENTS):
        start, end = index * step, (index + 1) * step
        x0, y0 = point(start)
        x1, y1 = point(end)
        dx0, dy0 = tangent(start)
        dx1, dy1 = tangent(end)
        commands.append(f"C{x0+dx0*step/3:.1f},{y0+dy0*step/3:.1f} "
                        f"{x1-dx1*step/3:.1f},{y1-dy1*step/3:.1f} {x1:.1f},{y1:.1f}")
    return "".join(commands) + "Z"


def render(theme, still=False, x=0, y=0, width=100, height=64,
           variant="exploration"):
    dark = theme == "dark"
    silver = "#b1bac4" if dark else "#59636e"
    ink = "#e6edf3" if dark else "#1f2328"
    animated, resting = [], []
    for strand in range(3):
        phase = pi / 3 if variant == "building" else pi / 5
        path = curve(phase, strand, variant)
        style = f'fill="none" stroke="{ink if strand == 1 else silver}" stroke-width="1.1" stroke-opacity="{.72 if strand == 1 else .3}" stroke-linejoin="round"'
        resting.append(f'<path d="{path}" {style}/>')
        if not still:
            frames = [curve(phase + 2 * pi * step / STEPS, strand, variant)
                      for step in range(STEPS)]
            frames.append(frames[0])
            animated.append(f'<path d="{path}" {style}><animate attributeName="d" dur="32s" repeatCount="indefinite" calcMode="linear" values="{";".join(frames)}"/></path>')
    if still:
        artwork = "".join(resting)
    else:
        artwork = f'''<style>
          .lissajous-rest {{ display:none }}
          @media(prefers-reduced-motion:reduce) {{
            .lissajous-motion {{ display:none }}
            .lissajous-rest {{ display:inline }}
          }}
        </style>
        <g class="lissajous-motion">{''.join(animated)}</g>
        <g class="lissajous-rest">{''.join(resting)}</g>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" x="{x}" y="{y}" width="{width}" height="{height}" viewBox="0 0 100 64" aria-hidden="true">
      {artwork}
    </svg>'''


def main():
    for variant in ("exploration", "building"):
        for theme in ("dark", "light"):
            for still in (False, True):
                suffix = "-still" if still else ""
                path = ROOT / f"assets/{variant}-motif-{theme}{suffix}.svg"
                path.write_text(render(theme, still, variant=variant) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
