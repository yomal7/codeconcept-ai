"""Turns a Diagram (nodes + edges, from the Presentation JSON) into an SVG string.

No coordinates ever come from the LLM. Layout is fully deterministic and
computed here in code -- the same "AI generates data, code renders
visuals" split the rest of the pipeline follows. Two layouts:

- "versus": exactly 2 nodes, comparison-type slides -> big side-by-side
  boxes with a VS badge between them.
- "chain": everything else -> boxes left-to-right (wrapping to a second
  row past 4 nodes) connected by arrows following the edge list.

Icons are real Lucide glyphs (renderer/icon_registry.py) shown inside a
colored "badge" circle -- not bare line art -- for visual weight. Font
sizes are never set inline here; every text element carries a CSS class
(dg-node text, dg-edge text, ...) so sizing lives entirely in
templates/styles/*.css, per the "components carry no inline styles"
principle.
"""

from backend.models import Diagram, DiagramNode
from renderer.icon_registry import get_icon

NODE_W, NODE_H = 300, 190
BADGE_R = 34
ICON_SIZE = 36
GAP = 60
MAX_LABEL_CHARS_PER_LINE = 16
MAX_LABEL_LINES = 3


def render_diagram_svg(diagram: Diagram, *, variant: str = "diagram") -> str:
    if variant == "comparison" and len(diagram.nodes) == 2:
        return _render_versus(diagram)
    return _render_chain(diagram)


# ---- chain layout (default: flows, sequences, generic diagrams) ------


def _render_chain(diagram: Diagram) -> str:
    nodes = diagram.nodes
    per_row = 4
    rows = [nodes[i : i + per_row] for i in range(0, len(nodes), per_row)] or [[]]

    row_width = max(len(row) for row in rows) * (NODE_W + GAP) - GAP
    canvas_w = row_width + GAP * 2
    canvas_h = len(rows) * (NODE_H + GAP * 2) + GAP

    positions: dict[str, tuple[float, float]] = {}
    parts: list[str] = []

    for row_index, row in enumerate(rows):
        row_w = len(row) * (NODE_W + GAP) - GAP
        start_x = (canvas_w - row_w) / 2
        y = GAP + row_index * (NODE_H + GAP * 2)
        for col_index, node in enumerate(row):
            x = start_x + col_index * (NODE_W + GAP)
            positions[node.id] = (x + NODE_W / 2, y + NODE_H / 2)
            parts.append(_node_svg(node, x, y))

    edges_svg = []
    for edge in diagram.edges:
        if edge.source not in positions or edge.target not in positions:
            continue
        edges_svg.append(_edge_svg(positions[edge.source], positions[edge.target], edge.label, NODE_W))

    return _wrap_svg(canvas_w, canvas_h, "\n".join(edges_svg) + "\n" + "\n".join(parts))


# ---- versus layout (comparison slides with exactly 2 nodes) ----------


def _render_versus(diagram: Diagram) -> str:
    left_node, right_node = diagram.nodes
    canvas_w = NODE_W * 2 + GAP * 3 + 140  # extra room for the VS badge
    canvas_h = NODE_H + GAP * 2

    left_x = GAP
    right_x = canvas_w - GAP - NODE_W
    y = GAP

    badge_cx = canvas_w / 2
    badge_cy = y + NODE_H / 2

    parts = [
        _node_svg(left_node, left_x, y, accent=True),
        _node_svg(right_node, right_x, y, accent=True),
        f"""<g class="dg-vs-badge">
            <circle cx="{badge_cx}" cy="{badge_cy}" r="42"/>
            <text x="{badge_cx}" y="{badge_cy}" text-anchor="middle" dominant-baseline="central">VS</text>
        </g>""",
    ]

    edge = diagram.edges[0] if diagram.edges else None
    if edge and edge.label:
        parts.append(
            f"""<text x="{badge_cx}" y="{y + NODE_H + 44}" text-anchor="middle"
                class="dg-caption">{_escape(edge.label)}</text>"""
        )
        canvas_h += 56

    return _wrap_svg(canvas_w, canvas_h, "\n".join(parts))


# ---- shared node/edge/text rendering ----------------------------------


def _node_svg(node: DiagramNode, x: float, y: float, *, accent: bool = False) -> str:
    css_class = "dg-node dg-node--accent" if accent else "dg-node"
    lines = _wrap_label(node.label)
    icon_cx, icon_cy = x + NODE_W / 2, y + 58

    text_start_y = icon_cy + BADGE_R + 34
    text_lines = "\n".join(
        f'<tspan x="{x + NODE_W / 2}" dy="{0 if i == 0 else 28}">{_escape(line)}</tspan>'
        for i, line in enumerate(lines)
    )

    return f"""<g class="{css_class}">
        <rect x="{x}" y="{y}" width="{NODE_W}" height="{NODE_H}" rx="20"/>
        {_icon_badge_svg(node.icon, icon_cx, icon_cy)}
        <text x="{x + NODE_W / 2}" y="{text_start_y}" text-anchor="middle" font-weight="600">
            {text_lines}
        </text>
    </g>"""


def _edge_svg(start: tuple[float, float], end: tuple[float, float], label: str | None, node_w: float) -> str:
    (x1, y1), (x2, y2) = start, end
    half_gap = node_w / 2 + 6
    if x2 > x1:
        x1, x2 = x1 + half_gap, x2 - half_gap
    elif x2 < x1:
        x1, x2 = x1 - half_gap, x2 + half_gap

    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
    label_svg = ""
    if label:
        label_svg = (
            f'<rect x="{mid_x - 90}" y="{mid_y - 34}" width="180" height="32" rx="16" class="dg-edge-label-bg"/>'
            f'<text x="{mid_x}" y="{mid_y - 18}" text-anchor="middle" dominant-baseline="central">{_escape(label)}</text>'
        )

    return f"""<g class="dg-edge">
        <path d="M {x1} {y1} L {x2} {y2}" marker-end="url(#dg-arrow)"/>
        {label_svg}
    </g>"""


def _wrap_svg(width: float, height: float, body: str) -> str:
    return f"""<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <marker id="dg-arrow" viewBox="0 0 10 10" refX="9" refY="5"
                    markerWidth="7" markerHeight="7" orient="auto-start-reverse">
                <path d="M 0 0 L 10 5 L 0 10 z" class="dg-arrowhead"/>
            </marker>
        </defs>
        {body}
    </svg>"""


def _wrap_label(label: str) -> list[str]:
    words = label.split()
    lines: list[str] = []
    current = ""

    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) <= MAX_LABEL_CHARS_PER_LINE:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
        if len(lines) == MAX_LABEL_LINES - 1:
            break
    if current:
        lines.append(current)

    if len(lines) < len(" ".join(words[len(lines) :]).split()) and len(lines) == MAX_LABEL_LINES:
        lines[-1] = lines[-1].rstrip() + "…"

    return lines[:MAX_LABEL_LINES]


def _escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _icon_badge_svg(icon_name: str | None, cx: float, cy: float) -> str:
    """A real Lucide icon centered inside a soft colored badge circle."""
    inner = get_icon(icon_name)
    half = ICON_SIZE / 2
    scale = ICON_SIZE / 24  # Lucide icons are natively drawn on a 24x24 grid
    return f"""<g>
        <circle cx="{cx}" cy="{cy}" r="{BADGE_R}" class="dg-icon-badge"/>
        <g class="dg-icon" transform="translate({cx - half},{cy - half}) scale({scale})">{inner}</g>
    </g>"""