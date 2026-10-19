"""Compose company lockups with a restrained, unfolding Prometheus mark."""

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
            "and branded apps.",
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


def animate_prometheus(logo):
    """Keep the original central dot fixed and unfold all satellites together."""
    svg = "{http://www.w3.org/2000/svg}"
    center = next(circle for circle in logo
                  if circle.get("cx") == "256" and circle.get("cy") == "268")
    origin = ET.SubElement(logo, svg + "g", {"transform": "translate(256 268)"})
    orbit = ET.SubElement(origin, svg + "g", {"class": "prometheus-orbit"})
    expansion = ET.SubElement(orbit, svg + "g", {"class": "prometheus-expand"})
    for circle in list(logo):
        if circle.tag != svg + "circle" or circle is center:
            continue
        logo.remove(circle)
        circle.set("cx", str(int(circle.get("cx")) - 256))
        circle.set("cy", str(int(circle.get("cy")) - 268))
        expansion.append(circle)
    # The original tight crop does not contain the mark's full rotating radius.
    logo.set("overflow", "visible")
    # Paint the stationary center last so the initial stack is one clean dot.
    logo.remove(center)
    logo.append(center)


def render(theme, mobile=False, still=False):
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
        if slug == "prometheus-vision" and not still:
            animate_prometheus(logo)
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
    motion = "" if still else '''<style>
    @keyframes prometheus-unfold {
      from { transform:scale(0) }
      to { transform:scale(1) }
    }
    @keyframes prometheus-turn {
      from { transform:rotate(0deg) }
      to { transform:rotate(360deg) }
    }
    .prometheus-expand {
      transform-origin:0 0;
      animation:prometheus-unfold .95s cubic-bezier(.22,1,.36,1) both;
    }
    .prometheus-orbit {
      transform-origin:0 0;
      animation:prometheus-turn 24s linear .95s infinite;
    }
    @media(prefers-reduced-motion:reduce) {
      .prometheus-expand,.prometheus-orbit { animation:none;transform:none }
    }
  </style>'''
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">Co-founder at Shredeo and Prometheus Vision</title>
  <desc id="desc">Shredeo: one platform for gyms and studios, from memberships and coaching to payments and branded apps. Prometheus Vision: software, AI and data, from business intelligence to custom apps and automation. Official monochrome logos.</desc>
  {motion}
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
            for still in (False, True):
                suffix = "-still" if still else ""
                (ROOT / f"assets/companies-{prefix}{theme}{suffix}.svg").write_text(
                    render(theme, mobile, still), encoding="utf-8")


if __name__ == "__main__":
    main()
