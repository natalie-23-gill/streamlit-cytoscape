# st-cytoscape

A Streamlit component for interactive graph visualization using Cytoscape.js.

## Features

Addresses key limitations from [st-link-analysis](https://github.com/AlrasheedA/st-link-analysis):

- **Custom Styling** - Pass any Cytoscape.js style property via `custom_styles`
- **Coordinate Positioning** - Position nodes with exact x/y coordinates
- **Multi-Tab Support** - Auto-resize when switching tabs
- **Custom Highlights** - Full control over selection appearance
- **Material Icons API** - Automatic icon validation and search via Google Material Icons API

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

### Material Icons Integration

st-cytoscape integrates with Google's Material Icons API to provide icon validation and search:

```python
from st_cytoscape import icons

# Search for icons
matching_icons = icons.search_icons("person")
print(matching_icons)  # ['person', 'person_outline', 'person_add', ...]

# Validate an icon name
is_valid = icons.is_valid_icon("person")  # True
is_valid = icons.is_valid_icon("invalid_icon")  # False

# Get all available icons
all_icons = icons.get_available_icons()

# Refresh icon list from Google API
icons.refresh_icons()
```

**Automatic Icon Validation:**

```python
# Validation is enabled by default - warns about invalid icons
NodeStyle("person", "#3498db", icon="person")  # No warning

NodeStyle("person", "#3498db", icon="invalid_icon")  # Warning in console

# Disable validation if needed
NodeStyle("person", "#3498db", icon="custom_icon", validate_icon=False)
```

**Benefits:**
- Automatic validation prevents typos in icon names
- Local caching reduces API calls
- Search functionality helps discover available icons
- Graceful fallback if API is unavailable

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

### `NodeStyle(type, color="#666", caption=None, icon=None, size=40, custom_styles=None, validate_icon=True)`

Defines visual styling for nodes.

**Parameters:**
- `type` - Node type identifier
- `color` - Node color (hex or name)
- `caption` - Property to use as label
- `icon` - Material icon name (validated by default)
- `size` - Node size in pixels
- `custom_styles` - Additional Cytoscape.js styles
- `validate_icon` - Enable/disable icon validation (default: True)

### `EdgeStyle(type, color="#666", caption=None, directed=False, width=2, custom_styles=None)`

### `HighlightStyle(node_border_color="#FFD700", node_border_width=3, edge_color=None, ...)`

### `create_node(id, label, node_type, x=None, y=None, **data)`

### `create_edge(id, source, target, edge_type, label=None, **data)`

### Material Icons API Functions

```python
from st_cytoscape import icons

icons.search_icons(query, force_refresh=False)  # Search for icons
icons.is_valid_icon(icon_name, force_refresh=False)  # Validate icon
icons.get_available_icons(force_refresh=False)  # Get all icons
icons.refresh_icons()  # Refresh from Google API
```

## Layouts

`cose` (default), `grid`, `circle`, `concentric`, `breadthfirst`, `preset`, and more.

## Examples

See `examples/` directory for full demos:

```bash
# Comprehensive feature demo
streamlit run examples/comprehensive_demo.py

# Material Icons API demo
streamlit run examples/icon_search_example.py

# Simple example
streamlit run examples/simple_example.py
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
