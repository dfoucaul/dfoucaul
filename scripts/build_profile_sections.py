"""Build two quiet, borderless SVG columns with monochrome brand symbols."""

from html import escape
from pathlib import Path
from xml.etree import ElementTree

from build_exploration_motif import render as exploration_motif

ROOT = Path(__file__).resolve().parents[1]


def brand_paths(slug):
    root = ElementTree.parse(ROOT / f"assets/icons/{slug}.svg").getroot()
    return "".join(f'<path d="{escape(node.attrib["d"], quote=True)}"/>'
                   for node in root.iter() if node.tag.endswith("}path"))


def render(kind, theme, still=False, width=330):
    dark = theme == "dark"
    foreground = "#e6edf3" if dark else "#1f2328"
    secondary = "#b1bac4" if dark else "#59636e"
    border = "#30363d" if dark else "#d1d9e0"
    background = "#0d1117" if dark else "#ffffff"
    heading = "I build with" if kind == "stack" else "I'm exploring"
    labels = (["Rust", "Go", "TypeScript", "Python"] if kind == "stack" else
              ["Machine learning", "AI & models", "Algorithms", "Data visualization", "Financial modeling", "M&A"])
    height = 235 if kind == "stack" else 285
    icons, rows = [], []
    for index, label in enumerate(labels):
        y = 77 + index * (44 if kind == "stack" else 34)
        if kind == "stack":
            icons.append(f'<g transform="translate(26 {y-19})">{brand_paths(label.lower())}</g>')
        text_x = 69 if kind == "stack" else 26
        rows.append(f'<text x="{text_x}" y="{y}" font-size="17" fill="{foreground}">{escape(label)}</text>')
    icon_markup = "".join(icons)
    compact = width < 220
    motif = exploration_motif(theme, still,
                              x=width-48 if compact else width-94,
                              y=4 if compact else -1,
                              width=36 if compact else 62,
                              height=30 if compact else 40,
                              variant="building" if kind == "stack" else "exploration")
    shimmer = ""
    if kind == "stack" and not still:
        shimmer = f'''<defs>
          <mask id="symbols" maskUnits="userSpaceOnUse" x="0" y="0" width="{width}" height="{height}"><g fill="white">{icon_markup}</g></mask>
          <linearGradient id="sheen"><stop stop-color="white" stop-opacity="0"/><stop offset=".5" stop-color="white"/><stop offset="1" stop-color="white" stop-opacity="0"/></linearGradient>
        </defs>
        <style>
          @keyframes sheen {{ 0%,25% {{ transform:translateX(-90px);opacity:0 }} 30% {{ opacity:.85 }} 55% {{ opacity:.85 }} 65%,100% {{ transform:translateX(345px);opacity:0 }} }}
          .sheen {{ animation:sheen 14s ease-in-out infinite }}
          @media(prefers-reduced-motion:reduce) {{ .sheen {{ display:none;animation:none }} }}
        </style>
        <g mask="url(#symbols)"><rect class="sheen" x="0" y="48" width="80" height="178" fill="url(#sheen)" opacity="0"/></g>'''
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
      <title id="title">{escape(heading)}</title>
      <desc id="desc">{escape(', '.join(labels))}.</desc>
      <rect width="{width}" height="{height}" fill="{background}"/>
      <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif">
        <text x="26" y="25" fill="{foreground}" font-size="18" font-weight="500">{escape(heading)}</text>
        <path d="M26 43H{width-26}" stroke="{border}" stroke-width=".65"/>
        <g fill="{secondary}">{icon_markup}</g>
        {''.join(rows)}
        {shimmer}
      </g>{motif}
    </svg>'''
    return "\n".join(line.rstrip() for line in svg.splitlines()) + "\n"


def main():
    for theme in ("dark", "light"):
        for kind in ("stack", "exploring"):
            (ROOT / f"assets/{kind}-{theme}.svg").write_text(render(kind, theme), encoding="utf-8")
            if kind == "stack":
                (ROOT / f"assets/{kind}-{theme}-still.svg").write_text(render(kind, theme, True), encoding="utf-8")


if __name__ == "__main__":
    main()
