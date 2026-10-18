"""A quiet, shared company composition, distinct from the animated portrait."""

from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET

from build_profile_header import embed

ROOT = Path(__file__).resolve().parents[1]
COMPANIES = (
    (
        "shredeo", "Shredeo",
        (
            "One platform for gyms and studios.",
            "Memberships, coaching, payments",
            "and branded apps, powered by AI.",
        ),
    ),
    (
        "prometheus-vision", "Prometheus Vision",
        (
            "Software, AI and data for businesses.",
            "From business intelligence to custom",
            "apps and intelligent automation.",
        ),
    ),
)


def render(theme, mobile=False):
    dark = theme == "dark"
    background = "#0d1117" if dark else "#ffffff"
    foreground = "#e6edf3" if dark else "#1f2328"
    secondary = "#a7adb6" if dark else "#59636e"
    border = "#30363d" if dark else "#d1d9e0"
    width, height = (400, 450) if mobile else (960, 260)
    label_x = 24 if mobile else 64
    label_y = 32 if mobile else 42
    panels = []
    for index, (slug, name, lines) in enumerate(COMPANIES):
        x = 24 if mobile else 64 + index * 480
        y = 68 + index * 220 if mobile else 84
        logo = ET.parse(ROOT / f"assets/brands/{slug}-mono.svg").getroot()
        logo.set("fill", foreground)
        # Crop only the original transparent padding, preserving the logo paths.
        viewbox = "52 30 159 190" if slug == "shredeo" else "82 75 341 387"
        logo_markup = embed(ET.tostring(logo, encoding="unicode"), slug,
                            x, y, 38, 44, viewbox)
        body = "".join(
            f'<text x="{x}" y="{y + 88 + line * 26}">{escape(text)}</text>'
            for line, text in enumerate(lines)
        )
        panels.append(f'''<g>
          {logo_markup}
          <text x="{x+58}" y="{y+32}" fill="{foreground}" font-size="27" font-weight="600" letter-spacing="-.65">{name}</text>
          <g fill="{secondary}" font-size="17">{body}</g>
        </g>''')
    # A single central seam defines columns, rather than another horizontal band.
    seam = "" if mobile else f'<path d="M480 83V238" stroke="{border}" stroke-width=".65"/>'
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">Co-founder at Shredeo and Prometheus Vision</title>
  <desc id="desc">Shredeo: one platform for gyms and studios, from memberships and coaching to payments, branded apps and AI. Prometheus Vision: software, AI and data, from business intelligence to custom apps and automation. Official monochrome logos.</desc>
  <rect width="{width}" height="{height}" fill="{background}"/>
  <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif">
    <text x="{label_x}" y="{label_y}" fill="{secondary}" font-size="12" letter-spacing="2.2">CO-FOUNDER</text>
    {''.join(panels)}
  </g>
  {seam}
</svg>
'''
    return "\n".join(line.rstrip() for line in svg.splitlines()) + "\n"


def main():
    for theme in ("dark", "light"):
        for mobile in (False, True):
            prefix = "mobile-" if mobile else ""
            (ROOT / f"assets/companies-{prefix}{theme}.svg").write_text(
                render(theme, mobile), encoding="utf-8")


if __name__ == "__main__":
    main()
