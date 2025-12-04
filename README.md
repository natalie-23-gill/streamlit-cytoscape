# st-cytoscape

A flexible, customizable Streamlit component for interactive graph visualization using Cytoscape.js.

## Overview

This project provides a Streamlit custom component for visualizing and interacting with graph data using Cytoscape.js. It supports customizable edge and node styles, labels, colors, captions, and icons.

## Features

- **Customizable Node and Edge Styles**: Easily define the appearance of nodes and edges using a variety of style options.
- **Material Icons Support**: Supports a subset of Material icons for styling nodes which can be passed by name (e.g., `icon='person'`). Custom icons can still be used by passing a URL (e.g., `icon='url(...)'`).
- **Customizable Layouts**: Choose from different layout algorithms to arrange the graph elements.
- **Interactive Features:**
  - Toolbar with fullscreen, JSON export, and layout refresh buttons.
  - View control bar for zooming, fitting, and centering the view.
  - View all properties of the selected elements in a side panel.
  - Highlights neighboring nodes or edges when an element is selected.
- **Node Actions (Expand / Remove):** Enable node removal and expansion using the `node_actions` parameter. Removal can be triggered by a delete keydown or a remove button click, while expansion occurs on a double-click or expand button click.

## Installation

```bash
pip install st-cytoscape
```

## Usage

```python
import streamlit as st
from st_cytoscape import st_cytoscape, NodeStyle, EdgeStyle

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
st.markdown("### st-cytoscape: Example")
st_cytoscape(elements, "cose", node_styles, edge_styles)
```

## API Reference

| Element        | Description                                                                                               |
| -------------- | --------------------------------------------------------------------------------------------------------- |
| `st_cytoscape` | Main component for creating and displaying the graph, including layout and height settings.               |
| `NodeStyle`    | Defines styles for nodes, including labels, colors, captions, and icons.                                  |
| `EdgeStyle`    | Defines styles for edges, including curve styles, labels, colors, and directionality.                     |
| `Event`        | Define an event to pass to component function and listen to.                                              |

## Development

Ensure you have Python 3.10+, Node.js, and npm installed.

### Setup

```bash
# Create conda environment
conda create -n st_cytoscape python=3.10
conda activate st_cytoscape

# Install Python package
poetry install

# Install frontend dependencies
cd src/st_cytoscape/frontend
npm install
```

### Running the App

Change `_RELEASE` flag in `src/st_cytoscape/component.py` to `False`.

In one terminal start the frontend dev server:

```bash
cd src/st_cytoscape/frontend
npm run start
```

In another terminal run the streamlit server:

```bash
cd examples
poetry run streamlit run app.py
```

### Testing

```bash
poetry run black .
poetry run flake8 st_cytoscape tests examples
poetry run mypy st_cytoscape
poetry run pytest
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`st_cytoscape` was created by Natalie Gill. It is licensed under the terms of the MIT license.

## Acknowledgments

This project is a fork of [st-link-analysis](https://github.com/AlrasheedA/st-link-analysis) by [@AlrasheedA](https://github.com/AlrasheedA), who developed the bulk of the original component. This fork extends the original with additional customization options.

- [st-link-analysis](https://github.com/AlrasheedA/st-link-analysis) - Original component
- [Cytoscape.js](https://js.cytoscape.org/)
- [Streamlit](https://www.streamlit.io/)
- [Material Icons](https://fonts.google.com/icons)
