"""Turns a Diagram (nodes + edges, from the Presentation JSON) into an SVG string.

No coordinates ever come from the LLM. Layout is fully deterministic and
computed here in code -- the same "AI generates data, code renders
visuals" split the rest of the pipeline follows. Two layouts:

- "versus": exactly 2 nodes, comparison-type slides -> big side-by-side
  boxes with a VS badge between them.
- "chain": everything else -> boxes left-to-right (wrapping to a second
  row past 4 nodes) connected by arrows following the edge list.
"""

from backend.models import Diagram, DiagramNode

NODE_W, NODE_H = 300, 190
ICON_SIZE = 56
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
            <text x="{badge_cx}" y="{badge_cy + 10}" text-anchor="middle" font-size="30">VS</text>
        </g>""",
    ]

    edge = diagram.edges[0] if diagram.edges else None
    if edge and edge.label:
        parts.append(
            f"""<text x="{badge_cx}" y="{y + NODE_H + 44}" text-anchor="middle"
                class="dg-caption" font-size="22">{_escape(edge.label)}</text>"""
        )
        canvas_h += 56

    return _wrap_svg(canvas_w, canvas_h, "\n".join(parts))


# ---- shared node/edge/text rendering ----------------------------------


def _node_svg(node: DiagramNode, x: float, y: float, *, accent: bool = False) -> str:
    css_class = "dg-node dg-node--accent" if accent else "dg-node"
    lines = _wrap_label(node.label)
    icon = _icon_svg(node.icon, x + NODE_W / 2, y + 54)

    text_start_y = y + 54 + ICON_SIZE / 2 + 36
    text_lines = "\n".join(
        f'<tspan x="{x + NODE_W / 2}" dy="{0 if i == 0 else 30}">{_escape(line)}</tspan>'
        for i, line in enumerate(lines)
    )

    return f"""<g class="{css_class}">
        <rect x="{x}" y="{y}" width="{NODE_W}" height="{NODE_H}" rx="20"/>
        {icon}
        <text x="{x + NODE_W / 2}" y="{text_start_y}" text-anchor="middle" font-size="24" font-weight="600">
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
            f'<text x="{mid_x}" y="{mid_y - 12}" text-anchor="middle" font-size="18">{_escape(label)}</text>'
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


# ---- icon library -------------------------------------------------------
# Small original line-art glyphs (not from any external icon set), keyed by
# the `icon` string the Planner puts in the JSON. Unknown/missing icons
# fall back to a circle with the label's first letter, so a new icon name
# the Planner invents never breaks rendering.

_ICONS = {
    "desktop": lambda cx, cy: f"""
        <rect x="{cx-26}" y="{cy-20}" width="52" height="34" rx="4"/>
        <line x1="{cx-14}" y1="{cy+22}" x2="{cx+14}" y2="{cy+22}"/>
        <line x1="{cx}" y1="{cy+14}" x2="{cx}" y2="{cy+22}"/>
    """,
    "server": lambda cx, cy: f"""
        <rect x="{cx-24}" y="{cy-26}" width="48" height="16" rx="3"/>
        <rect x="{cx-24}" y="{cy-6}" width="48" height="16" rx="3"/>
        <rect x="{cx-24}" y="{cy+14}" width="48" height="16" rx="3"/>
        <circle cx="{cx+14}" cy="{cy-18}" r="2" class="dg-icon-dot"/>
    """,
    "shield": lambda cx, cy: f"""
        <path d="M {cx} {cy-28} L {cx+24} {cy-18} L {cx+24} {cy+6}
                 C {cx+24} {cy+22} {cx+10} {cy+30} {cx} {cy+30}
                 C {cx-10} {cy+30} {cx-24} {cy+22} {cx-24} {cy+6}
                 L {cx-24} {cy-18} Z"/>
        <path d="M {cx-10} {cy} L {cx-3} {cy+8} L {cx+12} {cy-10}" class="dg-icon-stroke-only"/>
    """,
    "doc": lambda cx, cy: f"""
        <path d="M {cx-18} {cy-28} L {cx+8} {cy-28} L {cx+18} {cy-18} L {cx+18} {cy+28} L {cx-18} {cy+28} Z"/>
        <path d="M {cx+8} {cy-28} L {cx+8} {cy-18} L {cx+18} {cy-18}"/>
        <line x1="{cx-10}" y1="{cy-4}" x2="{cx+10}" y2="{cy-4}"/>
        <line x1="{cx-10}" y1="{cy+8}" x2="{cx+10}" y2="{cy+8}"/>
    """,
    "cloud": lambda cx, cy: f"""
        <path d="M {cx-24} {cy+12} a14 14 0 0 1 4 -27.4 a18 18 0 0 1 34 4.4
                 a12 12 0 0 1 -4 26 Z"/>
    """,
    "database": lambda cx, cy: f"""
        <ellipse cx="{cx}" cy="{cy-20}" rx="24" ry="9"/>
        <path d="M {cx-24} {cy-20} L {cx-24} {cy+16} A 24 9 0 0 0 {cx+24} {cy+16} L {cx+24} {cy-20}"/>
        <path d="M {cx-24} {cy-2} A 24 9 0 0 0 {cx+24} {cy-2}" class="dg-icon-stroke-only"/>
    """,
    "browser": lambda cx, cy: f"""
        <rect x="{cx-26}" y="{cy-22}" width="52" height="44" rx="5"/>
        <line x1="{cx-26}" y1="{cy-10}" x2="{cx+26}" y2="{cy-10}"/>
    """,
    "lock": lambda cx, cy: f"""
        <rect x="{cx-18}" y="{cy-2}" width="36" height="28" rx="5"/>
        <path d="M {cx-11} {cy-2} L {cx-11} {cy-14} A 11 11 0 0 1 {cx+11} {cy-14} L {cx+11} {cy-2}"
              class="dg-icon-stroke-only"/>
        <circle cx="{cx}" cy="{cy+12}" r="3" class="dg-icon-dot"/>
    """,
    "lock-road": lambda cx, cy: f"""
        <rect x="{cx-16}" y="{cy-24}" width="32" height="24" rx="5"/>
        <path d="M {cx-9} {cy-24} L {cx-9} {cy-32} A 9 9 0 0 1 {cx+9} {cy-32} L {cx+9} {cy-24}"
              class="dg-icon-stroke-only"/>
        <path d="M {cx-20} {cy+26} L {cx-6} {cy+2} L {cx+6} {cy+2} L {cx+20} {cy+26} Z"/>
        <line x1="{cx}" y1="{cy+8}" x2="{cx}" y2="{cy+20}" class="dg-icon-stroke-only"/>
    """,
    "mobile": lambda cx, cy: f"""
        <rect x="{cx-16}" y="{cy-28}" width="32" height="56" rx="6"/>
        <line x1="{cx-6}" y1="{cy+20}" x2="{cx+6}" y2="{cy+20}"/>
    """,
    "key": lambda cx, cy: f"""
        <circle cx="{cx-14}" cy="{cy}" r="12"/>
        <line x1="{cx-2}" y1="{cy}" x2="{cx+24}" y2="{cy}"/>
        <line x1="{cx+16}" y1="{cy}" x2="{cx+16}" y2="{cy+10}"/>
        <line x1="{cx+24}" y1="{cy}" x2="{cx+24}" y2="{cy+10}"/>
    """,
    "road": lambda cx, cy: f"""
        <path d="M {cx-20} {cy+28} L {cx-6} {cy-28} L {cx+6} {cy-28} L {cx+20} {cy+28} Z"/>
        <line x1="{cx}" y1="{cy-20}" x2="{cx}" y2="{cy-6}" class="dg-icon-stroke-only"/>
        <line x1="{cx}" y1="{cy+6}" x2="{cx}" y2="{cy+20}" class="dg-icon-stroke-only"/>
    """,
    "warning": lambda cx, cy: f"""
        <path d="M {cx} {cy-26} L {cx+24} {cy+20} L {cx-24} {cy+20} Z"/>
        <line x1="{cx}" y1="{cy-6}" x2="{cx}" y2="{cy+6}" class="dg-icon-stroke-only"/>
        <circle cx="{cx}" cy="{cy+13}" r="2" class="dg-icon-dot"/>
    """,
    "check": lambda cx, cy: f"""
        <circle cx="{cx}" cy="{cy}" r="26"/>
        <path d="M {cx-12} {cy} L {cx-2} {cy+10} L {cx+14} {cy-10}" class="dg-icon-stroke-only"/>
    """,
}


def _icon_svg(icon_name: str | None, cx: float, cy: float) -> str:
    builder = _ICONS.get((icon_name or "").lower())
    if builder is None:
        return f"""<circle cx="{cx}" cy="{cy}" r="26" class="dg-icon-fallback"/>"""
    return f'<g class="dg-icon">{builder(cx, cy)}</g>'