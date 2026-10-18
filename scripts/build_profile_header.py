"""Compose the existing animated avatar and two columns into a responsive header."""

from pathlib import Path
from xml.etree import ElementTree as ET

from build_gooey import render as avatar
from build_profile_sections import render as section

ROOT = Path(__file__).resolve().parents[1]
ET.register_namespace("", "http://www.w3.org/2000/svg")
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")


def embed(markup, prefix, x, y, width, height, viewbox=None):
    root = ET.fromstring(markup)
    identities = {node.attrib["id"]: f'{prefix}-{node.attrib["id"]}'
                  for node in root.iter() if "id" in node.attrib}
    for node in root.iter():
        for name, value in list(node.attrib.items()):
            if name == "id":
                node.set(name, identities[value])
            elif name == "aria-labelledby":
                node.set(name, " ".join(identities.get(part, part) for part in value.split()))
            else:
                for original, target in identities.items():
                    value = value.replace(f"url(#{original})", f"url(#{target})")
                node.set(name, value)
    root.set("x", str(x))
    root.set("y", str(y))
    root.set("width", str(width))
    root.set("height", str(height))
    if viewbox:
        root.set("viewBox", viewbox)
    return ET.tostring(root, encoding="unicode")


def render(theme, mobile=False, still=False):
    dark = theme == "dark"
    background = "#0d1117" if dark else "#ffffff"
    foreground = "#e6edf3" if dark else "#1f2328"
    if mobile:
        width, height = 400, 690
        portrait = embed(avatar(theme, still), "avatar", 20, 0, 360, 330, "140 0 360 360")
        stack = embed(section("stack", theme, still, 190), "stack", 5, 400, 190, 235)
        interests = embed(section("exploring", theme, still, 190), "interests", 205, 400, 190, 285)
        name_x, name_y = 200, 348
    else:
        width, height = 960, 370
        portrait = embed(avatar(theme, still), "avatar", 0, 0, 360, 360, "140 0 360 360")
        stack = embed(section("stack", theme, still, 240), "stack", 390, 55, 240, 235)
        interests = embed(section("exploring", theme, still, 280), "interests", 660, 55, 280, 285)
        name_x, name_y = 180, 345
    name = ET.parse(ROOT / "assets/name-instrument-serif.svg").getroot()
    name.set("color", foreground)
    name_width = float(name.attrib["width"])
    name_height = float(name.attrib["height"])
    baseline = float(name.attrib["data-baseline"])
    wordmark = embed(ET.tostring(name, encoding="unicode"), "name",
                     name_x - name_width / 2, name_y - baseline, name_width, name_height)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">
      <title id="title">Luz de Guada</title>
      <desc id="description">Animated Medusa in liquid silver. I build with Rust, Go, TypeScript and Python. I'm exploring machine learning, AI and models, algorithms, data visualization, financial modeling and M&amp;A.</desc>
      <rect width="{width}" height="{height}" fill="{background}"/>
      {portrait}
      {wordmark}
      {stack}
      {interests}
    </svg>'''
    return "\n".join(line.rstrip() for line in svg.splitlines()) + "\n"


def main():
    for theme in ("dark", "light"):
        for mobile in (False, True):
            for still in (False, True):
                prefix = "mobile-" if mobile else ""
                suffix = "-still" if still else ""
                path = ROOT / f"assets/header-{prefix}{theme}{suffix}.svg"
                path.write_text(render(theme, mobile, still), encoding="utf-8")


if __name__ == "__main__":
    main()
