# streamlit-cytoscape

A flexible, customizable Streamlit component for interactive graph visualization using Cytoscape.js. This project is a fork of [st-link-analysis](https://github.com/AlrasheedA/st-link-analysis) by [@AlrasheedA](https://github.com/AlrasheedA), who developed the bulk of the original component. This fork extends the original with additional customization options and bug fixes.


## Overview

This project provides a Streamlit custom component for visualizing and interacting with graph data using Cytoscape.js. It supports customizable edge and node styles, labels, colors, captions, and icons.

## Features

- **Customizable Node and Edge Styles**: Easily define the appearance of nodes and edges using a variety of style options.
- **Custom Styles Pass-through**: Use the `custom_styles` parameter on `NodeStyle` and `EdgeStyle` to pass any valid [Cytoscape.js style property](https://js.cytoscape.org/#style) directly, enabling fine-grained control over shapes, borders, opacity, fonts, and more.
- **Material Icons Support**: Supports a subset of Material icons for styling nodes which can be passed by name (e.g., `icon='person'`). Custom icons can still be used by passing a URL (e.g., `icon='url(...)'`).
- **Customizable Layouts**: Choose from different layout algorithms to arrange the graph elements.
- **Interactive Features:**
  - Toolbar with fullscreen, layout refresh, and export dialog (named file download with optional visual styles).
  - View control bar for zooming, fitting, and centering the view.
  - View all properties of the selected elements in a side panel.
  - Highlights neighboring nodes or edges when an element is selected.
- **Node Actions (Expand / Remove):** Enable node removal and expansion using the `node_actions` parameter. Removal can be triggered by a delete keydown or a remove button click, while expansion occurs on a double-click or expand button click.
- **Edge Actions (Collapse / Expand):** Collapse parallel edges (multiple edges between the same nodes) into a single meta-edge showing a priority label and count. Double-click to expand back to individual edges.
- **Infopanel Actions:** Add custom action buttons to the infopanel using `InfopanelAction`. When a selected element's action button is clicked, the action name and element data are returned to the Streamlit app.

## Installation

```bash
pip install streamlit-cytoscape
```

## Usage

```python
import streamlit as st
from streamlit_cytoscape import streamlit_cytoscape, NodeStyle, EdgeStyle

st.set_page_config(layout="wide")

# Sample Data
elements = {
    "nodes": [
        {"data": {"id": 1, "label": "PERSON", "name": "Streamlit"}},
        {"data": {"id": 2, "label": "PERSON", "name": "Hello"}},
        {"data": {"id": 3, "label": "PERSON", "name": "World"}},
        {"data": {"id": 4, "label": "POST", "content": "x"}},
        {"data": {"id": 5, "label": "POST", "content": "y"}},
    ],
    "edges": [
        {"data": {"id": 6, "label": "FOLLOWS", "source": 1, "target": 2}},
        {"data": {"id": 7, "label": "FOLLOWS", "source": 2, "target": 3}},
        {"data": {"id": 8, "label": "POSTED", "source": 3, "target": 4}},
        {"data": {"id": 9, "label": "POSTED", "source": 1, "target": 5}},
        {"data": {"id": 10, "label": "QUOTES", "source": 5, "target": 4}},
    ],
}

# Style node & edge groups
node_styles = [
    NodeStyle("PERSON", "#FF7F3E", "name", "person"),
    NodeStyle("POST", "#2A629A", "content", "description"),
]

edge_styles = [
    EdgeStyle("FOLLOWS", caption='label', directed=True),
    EdgeStyle("POSTED", caption='label', directed=True),
    EdgeStyle("QUOTES", caption='label', directed=True),
]

# Render the component
st.markdown("### streamlit-cytoscape: Example")
streamlit_cytoscape(elements, "cose", node_styles, edge_styles)
```

### Custom Styles

Use the `custom_styles` parameter to apply any valid Cytoscape.js style property:

```python
from streamlit_cytoscape import NodeStyle, EdgeStyle

# Custom node styling with borders, shapes, and fonts
node_styles = [
    NodeStyle(
        label="PERSON",
        color="#FF7F3E",
        caption="name",
        icon="person",
        custom_styles={
            "shape": "diamond",
            "width": 60,
            "height": 60,
            "border-width": 3,
            "border-color": "#000000",
            "border-style": "dashed",
            "opacity": 0.9,
            "font-size": 14,
            "color": "#FFFFFF",
        },
    ),
]

# Custom edge styling with line styles and arrows
edge_styles = [
    EdgeStyle(
        label="FOLLOWS",
        caption="label",
        directed=True,
        custom_styles={
            "width": 3,
            "line-style": "dashed",
            "opacity": 0.8,
            "target-arrow-shape": "vee",
            "arrow-scale": 1.5,
            "font-size": 10,
        },
    ),
]
```

See the [Cytoscape.js style documentation](https://js.cytoscape.org/#style) for all available properties.

### Edge Actions (Collapse / Expand Parallel Edges)

When your graph has multiple edges between the same pair of nodes, you can collapse them into a single "meta-edge" that shows a priority label and count:

```python
from streamlit_cytoscape import streamlit_cytoscape, NodeStyle, EdgeStyle

elements = {
    "nodes": [
        {"data": {"id": "alice", "label": "PERSON", "name": "Alice"}},
        {"data": {"id": "bob", "label": "PERSON", "name": "Bob"}},
    ],
    "edges": [
        # Multiple edges between Alice and Bob
        {"data": {"id": "e1", "label": "FOLLOWS", "source": "alice", "target": "bob"}},
        {"data": {"id": "e2", "label": "LIKES", "source": "alice", "target": "bob"}},
        {"data": {"id": "e3", "label": "WORKS_WITH", "source": "alice", "target": "bob"}},
    ],
}

# Collapse parallel edges on load, with FOLLOWS as priority label
streamlit_cytoscape(
    elements,
    layout="cose",
    edge_actions=["collapse", "expand"],
    collapse_parallel_edges=True,
    priority_edge_label="FOLLOWS",  # Shows "FOLLOWS (3)" on the meta-edge
)
```

You can also customize the appearance of collapsed meta-edges:

```python
streamlit_cytoscape(
    elements,
    layout="cose",
    edge_actions=["collapse", "expand"],
    collapse_parallel_edges=True,
    meta_edge_style={
        "line-color": "#FF0000",
        "width": 5,
        "font-weight": "bold",
    },
)
```

### Infopanel Actions

Add custom action buttons to the infopanel that appear when an element is selected. Clicking a button returns the action name and selected element data to your Streamlit app:

```python
from streamlit_cytoscape import (
    streamlit_cytoscape, NodeStyle, InfopanelAction,
)

actions = [
    InfopanelAction("ai_summary", "AI Summary", icon="science"),
    InfopanelAction("fetch_details", "Fetch Details", icon="analytics"),
    InfopanelAction("flag_review", "Flag for Review", icon="flag"),
]

def on_action():
    val = st.session_state["my_graph"]
    action = val["action"]       # e.g. "ai_summary"
    eid = val["data"]["element_id"]  # selected element ID
    # Update element data, call an API, etc.

streamlit_cytoscape(
    elements,
    layout="fcose",
    node_styles=node_styles,
    infopanel_actions=actions,
    on_change=on_action,
    key="my_graph",
)
```

### NetworkX Integration

You can pass a [NetworkX](https://networkx.org/) graph directly using `nx.cytoscape_data()`. Edge `source`/`target` values and missing edge `id` fields are automatically sanitized. Default node and edge colors are theme-aware, so graphs render correctly in both light and dark mode without any extra styling.

```python
import networkx as nx
from streamlit_cytoscape import streamlit_cytoscape

G = nx.karate_club_graph()
cyto_data = nx.cytoscape_data(G)

streamlit_cytoscape(
    elements=cyto_data["elements"],
    layout="cose",
)
```

This works with any NetworkX graph type, e.g. `nx.path_graph()`, `nx.complete_graph()`, `nx.from_pandas_edgelist()`.

If you want `NodeStyle`/`EdgeStyle` selectors to match, add a `label` field to your nodes/edges since `nx.cytoscape_data()` doesn't include one by default.

## API Reference

| Element        | Description                                                                                               |
| -------------- | --------------------------------------------------------------------------------------------------------- |
| `streamlit_cytoscape` | Main component for creating and displaying the graph, including layout and height settings.               |
| `NodeStyle`    | Defines styles for nodes, including labels, colors, captions, icons, and `custom_styles` for Cytoscape.js pass-through. |
| `EdgeStyle`    | Defines styles for edges, including curve styles, labels, colors, directionality, and `custom_styles` for Cytoscape.js pass-through. |
| `InfopanelAction` | Defines a custom action button for the infopanel with a name, label, and optional icon.                  |
| `Event`        | Define an event to pass to component function and listen to.                                              |

## Development

Ensure you have Python 3.11+, [uv](https://docs.astral.sh/uv/), Node.js, and npm installed.

### Setup

```bash
# Install the Python package and dev dependencies
# (uv creates and manages a virtual environment in .venv/)
uv sync

# Install frontend dependencies
cd src/streamlit_cytoscape/frontend
npm install
```

### Running the App

Change `_RELEASE` flag in `src/streamlit_cytoscape/component.py` to `False`.

In one terminal start the frontend dev server:

```bash
cd src/streamlit_cytoscape/frontend
npm run start
```

In another terminal run the streamlit server:

```bash
cd examples
uv run streamlit run app.py
```

### Testing

```bash
uv run black .
uv run flake8 src/streamlit_cytoscape tests examples
uv run mypy src/streamlit_cytoscape
uv run pytest
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`streamlit_cytoscape` was created by Natalie Gill. It is licensed under the terms of the MIT license.

## AI Disclosure Statement

Generative AI tools (Claude Code, Anthropic) were used as coding assistants during the development of this project. The authors maintain full responsibility for the accuracy of all code. AI-assisted outputs were reviewed and validated against expected behavior before integration. 


## Acknowledgments

This project is a fork of [st-link-analysis](https://github.com/AlrasheedA/st-link-analysis) by [@AlrasheedA](https://github.com/AlrasheedA), who developed the bulk of the original component. This fork extends the original with additional customization options.

- [st-link-analysis](https://github.com/AlrasheedA/st-link-analysis) - Original component
- [Cytoscape.js](https://js.cytoscape.org/)
- [Streamlit](https://www.streamlit.io/)
- [Material Icons](https://fonts.google.com/icons)
