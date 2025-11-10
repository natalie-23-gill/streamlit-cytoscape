# st-cytoscape

A Streamlit component for interactive graph visualization using Cytoscape.js.

## Features

Addresses key limitations from [st-link-analysis](https://github.com/AlrasheedA/st-link-analysis):

- **Custom Styling** - Pass any Cytoscape.js style property via `custom_styles`
- **Coordinate Positioning** - Position nodes with exact x/y coordinates
- **Multi-Tab Support** - Auto-resize when switching tabs
- **Custom Highlights** - Full control over selection appearance

## Installation

```bash
pip install streamlit-cytoscape
```

## Quick Start

```python
from st_cytoscape import st_cytoscape, NodeStyle, EdgeStyle, create_node, create_edge

elements = [
    create_node("a", "Alice", "person"),
    create_node("b", "Bob", "person"),
    create_edge("e1", "a", "b", "friends"),
]

event = st_cytoscape(
    elements=elements,
    node_styles=[NodeStyle("person", "#3498db", "label", size=50)],
    edge_styles=[EdgeStyle("friends", "#95a5a6", "label", directed=True)],
)
```

## Advanced Features

### Custom Styling

```python
NodeStyle("custom", "#9b59b6", custom_styles={
    "shape": "diamond",
    "border-width": 5,
    "border-color": "#34495e",
})

EdgeStyle("special", "#e74c3c", custom_styles={
    "line-style": "dashed",
    "curve-style": "bezier",
})
```

### Coordinate Positioning

```python
elements = [
    create_node("center", "Center", "hub", x=0, y=0),
    create_node("north", "North", "node", x=0, y=-200),
]

st_cytoscape(elements=elements, layout="preset")
```

### Custom Highlights

```python
from st_cytoscape import HighlightStyle

st_cytoscape(
    elements=elements,
    highlight_style=HighlightStyle(
        node_border_color="#FFD700",
        node_border_width=4,
        edge_color="#FF6347"
    )
)
```

### Multi-Tab Support

```python
tab1, tab2 = st.tabs(["Graph 1", "Graph 2"])
with tab1:
    st_cytoscape(elements=elements1)
with tab2:
    st_cytoscape(elements=elements2)
```

## API Reference

### `st_cytoscape(elements, node_styles=None, edge_styles=None, layout="cose", height=600, ...)`

Main component for rendering graphs.

**Key Parameters:**
- `elements` - List of nodes and edges
- `node_styles` - List of NodeStyle objects
- `edge_styles` - List of EdgeStyle objects
- `layout` - Layout algorithm (cose, grid, circle, breadthfirst, preset)
- `highlight_style` - HighlightStyle for selections
- `selection_type` - "single", "additive", or "none"
- `auto_resize` - Auto-resize on container changes (default: True)

**Returns:** Event dict with type, target, and selected elements

### `NodeStyle(type, color="#666", caption=None, icon=None, size=40, custom_styles=None)`

### `EdgeStyle(type, color="#666", caption=None, directed=False, width=2, custom_styles=None)`

### `HighlightStyle(node_border_color="#FFD700", node_border_width=3, edge_color=None, ...)`

### `create_node(id, label, node_type, x=None, y=None, **data)`

### `create_edge(id, source, target, edge_type, label=None, **data)`

## Layouts

`cose` (default), `grid`, `circle`, `concentric`, `breadthfirst`, `preset`, and more.

## Examples

See `examples/` directory. Run with:

```bash
streamlit run examples/comprehensive_demo.py
```

## Development

```bash
pip install -e .
cd frontend && npm install && npm start
```

Build: `cd frontend && npm run build`

## License

MIT License

## Contributing

Issues and pull requests welcome. See CONTRIBUTING.md for details.

Built upon [st-link-analysis](https://github.com/AlrasheedA/st-link-analysis) with community-requested enhancements.
