#!/usr/bin/env python3

import sys
from pathlib import Path
import frontmatter


def field_datatype(dataset, field):
    if field.endswith("-date") or field.endswith("Date"):
        return "date"
    elif field.endswith("-url") or field.endswith("URI"):
        return "url"
    elif field in ["point", "geometry"]:
        return "wkt"
    elif field in datasets and field != dataset:
        return "reference"
    else:
        return "string"


def svg_rect(c, X, Y, h, v):
    return f'<rect x="{X}" y="{Y}" width="{h}" height="{v}" class="{c}"/>'


def svg_text(c, text, X, Y):
    return f'<text x="{X}" y="{Y}" class="{c}">{text}</text>'


def svg_spline(c, from_x, from_y, to_x, to_y):
    mid_x = min(from_x, to_x) + abs(from_x - to_x) / 2
    return (
        f'<path class="{c}" fill="none" stroke-width="2"'
        f' marker-start="url(#start-dot)" marker-end="url(#end-dot)"'
        f' d="M {from_x} {from_y} C {mid_x} {from_y} {mid_x} {to_y} {to_x} {to_y}"/>'
    )


path = Path(sys.argv[1])
spec = frontmatter.load(path)
row = spec.metadata

row_height = 20
text_y = int(row_height / 2)
padding = 5

field_width = 162
datatype_width = 52
gap = 80

row_width = field_width + datatype_width


datasets = [d["dataset"] for d in row["datasets"]]
maxrows = max([len(d["fields"]) for d in row["datasets"]])
ndatasets = len(datasets)
ngaps = ndatasets - 1
canvas_width = ndatasets * row_width + ngaps * gap
canvas_height = (maxrows + 1) * row_height

X = 0
points = {}
links = []
boxes = []

for d in row["datasets"]:
    dataset = d["dataset"]

    Y = 0
    box = []
    box.append(svg_rect("name", X, Y, row_width, row_height))
    box.append(svg_text("name", dataset, X + int(row_width / 2), Y + text_y))

    for f in d["fields"]:
        field = f["field"]
        datatype = field_datatype(dataset, field)

        Y = Y + row_height

        box.append(svg_rect("field", X, Y, field_width, row_height))
        box.append(svg_rect("datatype", X + field_width, Y, datatype_width, row_height))

        box.append(svg_text("field", field, X + padding, Y + text_y))
        box.append(
            svg_text("datatype", datatype, X + field_width + padding, Y + text_y)
        )

        points[f"from:{dataset}:{field}"] = (X, Y + text_y)
        points[f"to:{dataset}:{field}"] = (X + row_width, Y + text_y)

        if field in datasets:
            links.append(
                {"from": f"from:{dataset}:{field}", "to": f"to:{field}:reference"}
            )

    boxes.append(box)

    X = X + row_width + gap


print(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_width}" height="{canvas_height}">'
)
print(
    """<defs>
<style>
text{font-family:sans-serif; font-size:10px; dominant-baseline:middle;}
text.name{fill:#fff;font-weight:700;text-anchor:middle}
rect.name{fill:#0b0c0c; stroke:#0b0c0c;}
rect{fill:#fff;stroke:#b1b4b6;}
text.field{fill:#0b0c0c;}
text.datatype{fill:#0b0c0c;}
.line{stroke:#0b0c0c;}
</style>
<marker id="start-dot" markerWidth="6" markerHeight="6" refX="3" refY="3" markerUnits="strokeWidth">
  <circle cx="3" cy="3" r="2" fill="#fff" stroke="#0b0c0c"/>
</marker>
<marker id="end-dot" markerWidth="6" markerHeight="6" refX="3" refY="3" markerUnits="strokeWidth">
  <circle cx="3" cy="3" r="2" fill="#0b0c0c" />
</marker>
<marker id="end-arrow" markerWidth="6" markerHeight="6" refX="6.25" refY="3" orient="auto" markerUnits="strokeWidth">
  <polyline points="0 0 6 3 0 6" fill="none" stroke="#0b0c0c"/>
</marker>
</defs>"""
)

for l in links:
    print(svg_spline("line", *points[l["from"]], *points[l["to"]]))

for box in boxes:
    print("<g>")
    print("\n".join(box))
    print("</g>")

print("</svg>")
