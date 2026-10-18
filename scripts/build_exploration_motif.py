"""Original phase-shifting Lissajous curves, rendered as a self-contained SVG."""

from math import pi, sin
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = 128
STEPS = 16


def curve(phase, strand):
    points = []
    for index in range(SAMPLES):
        t = 2 * pi * index / SAMPLES
        # Different frequencies produce a closed figure; phase changes its shape.
        x = 50 + 39 * sin(3 * t + phase + strand * .11)
        y = 32 + 25 * sin(2 * t + strand * .08)
        points.append(f"{x:.2f},{y:.2f}")
    return "M" + "L".join(points) + "Z"


def render(theme, still=False, x=0, y=0, width=100, height=64):
    dark = theme == "dark"
    silver = "#b1bac4" if dark else "#59636e"
    ink = "#e6edf3" if dark else "#1f2328"
    animated, resting = [], []
    for strand in range(3):
        phase = pi / 5
        path = curve(phase, strand)
        style = f'fill="none" stroke="{ink if strand == 1 else silver}" stroke-width="1.1" stroke-opacity="{.72 if strand == 1 else .3}" stroke-linejoin="round"'
        resting.append(f'<path d="{path}" {style}/>')
        if not still:
            frames = [curve(phase + 2 * pi * step / STEPS, strand)
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
    for theme in ("dark", "light"):
        for still in (False, True):
            suffix = "-still" if still else ""
            path = ROOT / f"assets/exploration-motif-{theme}{suffix}.svg"
            path.write_text(render(theme, still) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
