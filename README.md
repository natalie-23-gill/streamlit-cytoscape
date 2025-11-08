# st-cytoscape

A flexible Streamlit component for interactive graph visualization using Cytoscape.js with enhanced customization options.

## 🎯 Why st-cytoscape?

This project addresses several limitations and open issues in [st-link-analysis](https://github.com/AlrasheedA/st-link-analysis) that are not being actively addressed:

### Issues Resolved

✅ **[PR #62](https://github.com/AlrasheedA/st-link-analysis/pull/62)** - Custom Styling Support
- Built-in `custom_styles` parameter for nodes and edges
- Pass any Cytoscape.js style property directly

✅ **[Issue #44](https://github.com/AlrasheedA/st-link-analysis/issues/44)** - Node Placement with Coordinates
- Position nodes using exact x/y coordinates
- Support for preset layouts with manual positioning

✅ **[Issue #35](https://github.com/AlrasheedA/st-link-analysis/issues/35)** - Dynamic Resizing in Multi-Tab Scenarios
- Automatic resize detection using ResizeObserver
- Properly renders graphs when switching between Streamlit tabs

✅ **[Issue #63](https://github.com/AlrasheedA/st-link-analysis/issues/63)** - Customizable Highlight Styles
- Full control over selection highlight appearance
- Custom colors, borders, and widths for selected elements

## 🚀 Installation

```bash
pip install streamlit-cytoscape
```

Or install from source:

```bash
git clone https://github.com/natalie-23-gill/st-cytoscape.git
cd st-cytoscape
pip install -e .
```

## 📖 Quick Start

```python
import streamlit as st
from st_cytoscape import st_cytoscape, NodeStyle, EdgeStyle, create_node, create_edge

# Create graph elements
elements = [
    create_node("alice", "Alice", "person"),
    create_node("bob", "Bob", "person"),
    create_edge("e1", "alice", "bob", "friends", "knows"),
]

# Define styles
node_styles = [
    NodeStyle("person", "#3498db", "label", "person", size=50)
]

edge_styles = [
    EdgeStyle("friends", "#95a5a6", "label", directed=True, width=3)
]

# Render the graph
event = st_cytoscape(
    elements=elements,
    node_styles=node_styles,
    edge_styles=edge_styles,
    layout="cose",
    height=500
)
```

## 🎨 Advanced Features

### Custom Styling (PR #62)

Pass any Cytoscape.js style property using `custom_styles`:

```python
NodeStyle(
    type="custom",
    color="#9b59b6",
    custom_styles={
        "shape": "diamond",
        "border-width": 5,
        "border-color": "#34495e",
        "background-opacity": 0.8,
    }
)

EdgeStyle(
    type="special",
    color="#e74c3c",
    custom_styles={
        "line-style": "dashed",
        "curve-style": "bezier",
    }
)
```

### Coordinate Positioning (Issue #44)

Position nodes with exact coordinates:

```python
# Method 1: Using create_node helper
elements = [
    create_node("center", "Center", "hub", x=0, y=0),
    create_node("north", "North", "node", x=0, y=-200),
    create_node("east", "East", "node", x=200, y=0),
]

# Use preset layout to honor positions
st_cytoscape(
    elements=elements,
    layout="preset",
    ...
)
```

### Custom Highlight Styles (Issue #63)

Customize how selected elements appear:

```python
from st_cytoscape import HighlightStyle

highlight = HighlightStyle(
    node_border_color="#FFD700",
    node_border_width=4,
    edge_color="#FF6347",
    edge_width=5,
    custom_styles={
        "background-opacity": 1.0,
    }
)

st_cytoscape(
    elements=elements,
    highlight_style=highlight,
    ...
)
```

### Multi-Tab Support (Issue #35)

The component automatically resizes when used in Streamlit tabs:

```python
tab1, tab2 = st.tabs(["Graph 1", "Graph 2"])

with tab1:
    st_cytoscape(elements=elements1, auto_resize=True, ...)

with tab2:
    st_cytoscape(elements=elements2, auto_resize=True, ...)
```

## 📚 API Reference

### `st_cytoscape()`

Main component function.

**Parameters:**
- `elements` (List[Dict]): Node and edge elements in Cytoscape.js format
- `node_styles` (List[NodeStyle], optional): Styling for different node types
- `edge_styles` (List[EdgeStyle], optional): Styling for different edge types
- `layout` (str, default="cose"): Layout algorithm (cose, grid, circle, breadthfirst, etc.)
- `height` (int|str, default=600): Component height
- `width` (int|str, default="100%"): Component width
- `selection_type` (str, default="single"): Selection mode (single, additive, none)
- `highlight_style` (HighlightStyle, optional): Custom highlight styling
- `enable_physics` (bool, default=True): Enable physics-based layouts
- `pan_enabled` (bool, default=True): Allow panning
- `zoom_enabled` (bool, default=True): Allow zooming
- `boxselection_enabled` (bool, default=False): Allow box selection
- `auto_resize` (bool, default=True): Auto-resize on container changes
- `key` (str, optional): Streamlit component key

**Returns:**
- `Dict`: Event data with type, target, and selected elements

### `NodeStyle`

Defines node appearance.

**Parameters:**
- `type` (str): Node type identifier
- `color` (str, default="#666"): Node color
- `caption` (str, optional): Property to display as label
- `icon` (str, optional): Material icon name
- `size` (int, default=40): Node size in pixels
- `position` (Dict, optional): Fixed position with x, y coordinates
- `custom_styles` (Dict, optional): Additional Cytoscape.js styles

### `EdgeStyle`

Defines edge appearance.

**Parameters:**
- `type` (str): Edge type identifier
- `color` (str, default="#666"): Edge color
- `caption` (str, optional): Property to display as label
- `directed` (bool, default=False): Show directional arrow
- `width` (int, default=2): Edge width in pixels
- `custom_styles` (Dict, optional): Additional Cytoscape.js styles

### `HighlightStyle`

Defines selection highlight appearance.

**Parameters:**
- `node_color` (str, optional): Color for highlighted nodes
- `node_border_width` (int, default=3): Border width for highlighted nodes
- `node_border_color` (str, default="#FFD700"): Border color for highlighted nodes
- `edge_color` (str, optional): Color for highlighted edges
- `edge_width` (int, optional): Width for highlighted edges
- `custom_styles` (Dict, optional): Additional Cytoscape.js styles

### Helper Functions

#### `create_node(id, label, node_type, x=None, y=None, **additional_data)`

Creates a node element with optional positioning.

#### `create_edge(id, source, target, edge_type, label=None, **additional_data)`

Creates an edge element.

## 🎯 Supported Layouts

- `cose` - Physics-based layout (default)
- `grid` - Grid layout
- `circle` - Circular layout
- `concentric` - Concentric circles
- `breadthfirst` - Tree/hierarchy layout
- `preset` - Use provided node positions
- And more from Cytoscape.js

## 📝 Examples

See the `examples/` directory for complete examples:

- `simple_example.py` - Basic usage
- `comprehensive_demo.py` - All features demonstrated with multi-tab support

Run an example:

```bash
streamlit run examples/comprehensive_demo.py
```

## 🔧 Development

### Setup

```bash
# Install Python dependencies
pip install -e .

# Install frontend dependencies
cd frontend
npm install

# Start development server
npm start
```

### Building

```bash
cd frontend
npm run build
```

## 🤝 Comparison with st-link-analysis

| Feature | st-link-analysis | st-cytoscape |
|---------|------------------|--------------|
| Custom Cytoscape.js styles | ❌ (PR pending) | ✅ Built-in |
| Coordinate positioning | ❌ | ✅ |
| Multi-tab auto-resize | ❌ (Issue #35) | ✅ |
| Custom highlight styles | ❌ (Issue #63) | ✅ |
| Material icons | ✅ | ✅ |
| Layout algorithms | ✅ | ✅ |
| Interactive events | ✅ | ✅ |

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

This project builds on concepts from [st-link-analysis](https://github.com/AlrasheedA/st-link-analysis) by AlrasheedA, extending it with features requested by the community.

## 🐛 Issues & Contributing

Found a bug or have a feature request? Please open an issue on GitHub.

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
