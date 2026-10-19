"""Isolate static SVG artwork so image renderers can reuse it during animation.

The layer remains vector, including the outlined signature and monochrome
icons. No browser script, external resource or rasterized text is required.
"""

import base64
from copy import deepcopy
from xml.etree import ElementTree as ET

SVG = "{http://www.w3.org/2000/svg}"


def cache_static_layer(markup):
    root = ET.fromstring(markup)
    plate = deepcopy(root)
    for child in list(plate):
        if child.tag == SVG + "rect":
            plate.remove(child)
        elif child.tag == SVG + "svg":
            label = child.get("aria-labelledby", "")
            if label.startswith("avatar-"):
                plate.remove(child)
            elif label.startswith(("stack-", "interests-")):
                for item in list(child):
                    if item.tag in (SVG + "rect", SVG + "svg"):
                        child.remove(item)
                    elif item.tag == SVG + "g":
                        for node in list(item):
                            if node.tag in (SVG + "defs", SVG + "style") or node.get("mask"):
                                item.remove(node)

    for child in list(root):
        if child.tag != SVG + "svg":
            continue
        label = child.get("aria-labelledby", "")
        if label.startswith("name-"):
            root.remove(child)
        elif label.startswith(("stack-", "interests-")):
            for item in list(child):
                if item.tag == SVG + "rect":
                    child.remove(item)
                elif item.tag == SVG + "g":
                    for node in list(item):
                        if node.tag not in (SVG + "defs", SVG + "style") and not node.get("mask"):
                            item.remove(node)

    data = base64.b64encode(ET.tostring(plate, encoding="utf-8")).decode("ascii")
    layer = ET.Element(SVG + "image", {
        "x": "0", "y": "0", "width": root.get("width"), "height": root.get("height"),
        "href": "data:image/svg+xml;base64," + data, "aria-hidden": "true",
    })
    # The plate is above the avatar canvas, below the moving motif/sheen layers.
    avatar = next(child for child in root
                  if child.get("aria-labelledby", "").startswith("avatar-"))
    root.insert(list(root).index(avatar) + 1, layer)
    return ET.tostring(root, encoding="unicode")
