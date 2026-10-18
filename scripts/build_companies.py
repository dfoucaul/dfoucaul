"""Original monochrome company portraits using the actual company logo paths."""

from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET

from build_profile_header import embed

ROOT = Path(__file__).resolve().parents[1]
COMPANIES = {
    "shredeo": {
        "name": "Shredeo",
        "site": "https://shredeo.com/",
        "desktop": [
            "An all-in-one platform for gyms and studios.",
            "Memberships, coaching, payments and branded apps,",
            "connected by AI-powered automation.",
        ],
        "mobile": [
            "One platform for gyms and studios.",
            "Memberships, coaching and payments.",
            "Branded member apps and AI automation.",
        ],
        "email": "foucauld@shredeo.com",
        "delay": "0s",
    },
    "prometheus-vision": {
        "name": "Prometheus Vision",
        "site": "https://prometheus-vision.com/en",
        "desktop": [
            "Software engineering, AI and data for real businesses.",
            "From business intelligence to intelligent automation,",
            "built directly with the developers behind the work.",
        ],
        "mobile": [
            "Custom software, AI and data solutions.",
            "From business intelligence to bespoke apps,",
            "built directly with the developers behind them.",
        ],
        "email": "fdelahaye@prometheus-vision.com",
        "delay": "-7s",
    },
}


def render(slug, theme, mobile=False, still=False):
    company = COMPANIES[slug]
    dark = theme == "dark"
    background = "#0d1117" if dark else "#ffffff"
    foreground = "#e6edf3" if dark else "#1f2328"
    secondary = "#a7adb6" if dark else "#59636e"
    border = "#30363d" if dark else "#d1d9e0"
    disc = "#12171d" if dark else "#f5f6f8"
    highlight = "#f5f5f7" if dark else "#636d78"
    width, height = (360, 370) if mobile else (960, 250)
    cx, cy = (180, 98) if mobile else (180, 124)
    role_x, role_y = (180, 195) if mobile else (416, 48)
    text_anchor = "middle" if mobile else "start"
    title = ET.parse(ROOT / f"assets/brands/{slug}-title.svg").getroot()
    title.set("color", foreground)
    title_scale = 34 / 36 if mobile else 1
    title_width = float(title.attrib["width"]) * title_scale
    title_height = float(title.attrib["height"]) * title_scale
    baseline = float(title.attrib["data-baseline"]) * title_scale
    title_x, title_y = ((180-title_width/2), 234) if mobile else (416, 96)
    title_markup = embed(ET.tostring(title, encoding="unicode"), "company-name",
                         title_x, title_y-baseline, title_width, title_height)
    logo = ET.parse(ROOT / f"assets/brands/{slug}-mono.svg").getroot()
    logo.set("fill", "url(#silver)")
    logo_markup = embed(ET.tostring(logo, encoding="unicode"), "brand",
                        cx-64, cy-64, 128, 128)
    lines = company["mobile" if mobile else "desktop"]
    text_x = 180 if mobile else 416
    text_y = 274 if mobile else 140
    line_height = 23 if mobile else 26
    text_size = 14 if mobile else 18
    body = "".join(f'<text x="{text_x}" y="{text_y+index*line_height}" text-anchor="{text_anchor}">{escape(line)}</text>'
                   for index, line in enumerate(lines))
    motion = "" if still else f'''<style>
      @keyframes orbit {{ to {{ stroke-dashoffset:-477.52 }} }}
      .orbit {{ animation:orbit 18s {company['delay']} linear infinite }}
      @media(prefers-reduced-motion:reduce) {{ .orbit {{ animation:none }} }}
    </style>'''
    description = escape(f"Co-founder at {company['name']}. {' '.join(lines)}")
    line_x, line_right = (24, 336) if mobile else (36, 924)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
      <title id="title">{company['name']}</title>
      <desc id="desc">{description}</desc>
      <defs>
        <linearGradient id="silver" x1="0" y1="0" x2="1" y2="1">
          <stop stop-color="{foreground}"/><stop offset=".45" stop-color="{highlight}"/><stop offset="1" stop-color="{secondary}"/>
        </linearGradient>
        <linearGradient id="thread" x1="0" y1="0" x2="0" y2="1">
          <stop stop-color="{secondary}" stop-opacity="0"/><stop offset=".5" stop-color="{secondary}" stop-opacity=".45"/><stop offset="1" stop-color="{secondary}" stop-opacity="0"/>
        </linearGradient>
        <pattern id="print" width="4" height="4" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".45" fill="{foreground}" fill-opacity=".12"/></pattern>
      </defs>
      {motion}
      <rect width="{width}" height="{height}" fill="{background}"/>
      <path d="M{cx} 0V{cy-80}" stroke="url(#thread)" stroke-width=".65"/>
      <circle cx="{cx}" cy="{cy}" r="72" fill="{disc}" stroke="{border}" stroke-width=".7"/>
      <circle cx="{cx}" cy="{cy}" r="68" fill="url(#print)"/>
      <circle cx="{cx}" cy="{cy}" r="76" fill="none" stroke="{border}" stroke-width=".65"/>
      <circle class="orbit" cx="{cx}" cy="{cy}" r="76" fill="none" stroke="{highlight}" stroke-opacity=".75" stroke-width="1" stroke-dasharray="32 445.52" stroke-linecap="round"/>
      {logo_markup}
      <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif">
        <text x="{role_x}" y="{role_y}" text-anchor="{text_anchor}" fill="{secondary}" font-size="10" letter-spacing="2.1">CO-FOUNDER</text>
        {title_markup}
        <g fill="{secondary}" font-size="{text_size}">{body}</g>
      </g>
      <path d="M{line_x} {height-1}H{line_right}" stroke="{border}" stroke-width=".6"/>
    </svg>'''
    return "\n".join(line.rstrip() for line in svg.splitlines()) + "\n"


def main():
    for slug in COMPANIES:
        for theme in ("dark", "light"):
            for mobile in (False, True):
                for still in (False, True):
                    prefix = "mobile-" if mobile else ""
                    suffix = "-still" if still else ""
                    path = ROOT / f"assets/company-{slug}-{prefix}{theme}{suffix}.svg"
                    path.write_text(render(slug, theme, mobile, still), encoding="utf-8")


if __name__ == "__main__":
    main()
