"""
Main Streamlit component for st-cytoscape
"""

import streamlit.components.v1 as components
import os
from typing import List, Dict, Any, Optional, Union
from .styles import NodeStyle, EdgeStyle, HighlightStyle
from .events import Event

# Determine if we're in development mode
_RELEASE = True
_COMPONENT_NAME = "st_cytoscape"

if not _RELEASE:
    _component_func = components.declare_component(
        _COMPONENT_NAME,
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component(_COMPONENT_NAME, path=build_dir)


def st_cytoscape(
    elements: List[Dict[str, Any]],
    node_styles: Optional[List[NodeStyle]] = None,
    edge_styles: Optional[List[EdgeStyle]] = None,
    layout: str = "cose",
    height: Union[int, str] = 600,
    width: Union[int, str] = "100%",
    selection_type: str = "single",
    highlight_style: Optional[HighlightStyle] = None,
    enable_physics: bool = True,
    pan_enabled: bool = True,
    zoom_enabled: bool = True,
    boxselection_enabled: bool = False,
    auto_resize: bool = True,
    key: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Create an interactive graph visualization using Cytoscape.js

    This component addresses several issues from st-link-analysis:
    - Issue #44: Node positioning with coordinates
    - Issue #35: Dynamic resizing in multi-tab scenarios
    - Issue #63: Customizable highlight styles
    - PR #62: Built-in custom_styles support

    Args:
        elements: List of node and edge dictionaries in Cytoscape.js format
                 Nodes: {"data": {"id": "n1", "label": "Node 1", "type": "person", ...}}
                 Edges: {"data": {"id": "e1", "source": "n1", "target": "n2", "type": "knows", ...}}
        node_styles: List of NodeStyle objects defining node appearance by type
        edge_styles: List of EdgeStyle objects defining edge appearance by type
        layout: Layout algorithm (cose, grid, circle, concentric, breadthfirst, cola, etc.)
        height: Component height in pixels or CSS string (e.g., "100vh")
        width: Component width in pixels or CSS string (e.g., "100%")
        selection_type: "single", "additive", or "none"
        highlight_style: HighlightStyle object for customizing element highlights
        enable_physics: Enable physics-based layouts
        pan_enabled: Allow panning the graph
        zoom_enabled: Allow zooming
        boxselection_enabled: Allow box selection
        auto_resize: Automatically resize when container changes (fixes Issue #35)
        key: Streamlit component key

    Returns:
        Dictionary containing event data and selected elements, or None
    """
    # Process styles
    node_styles_dict = [style.to_dict() for style in (node_styles or [])]
    edge_styles_dict = [style.to_dict() for style in (edge_styles or [])]
    highlight_dict = highlight_style.to_dict() if highlight_style else None

    # Process elements to handle coordinate positioning
    processed_elements = []
    for elem in elements:
        elem_copy = dict(elem)

        # Handle node positioning from NodeStyle
        if "data" in elem_copy and "position" not in elem_copy:
            node_type = elem_copy["data"].get("type")
            if node_type:
                # Find matching node style
                for style_dict in node_styles_dict:
                    if style_dict["type"] == node_type and style_dict.get("position"):
                        elem_copy["position"] = style_dict["position"]
                        break

        # Handle coordinate positioning from element data
        if "data" in elem_copy:
            data = elem_copy["data"]
            if "x" in data and "y" in data and "position" not in elem_copy:
                elem_copy["position"] = {"x": data["x"], "y": data["y"]}

        processed_elements.append(elem_copy)

    component_value = _component_func(
        elements=processed_elements,
        node_styles=node_styles_dict,
        edge_styles=edge_styles_dict,
        layout=layout,
        height=height,
        width=width,
        selection_type=selection_type,
        highlight_style=highlight_dict,
        enable_physics=enable_physics,
        pan_enabled=pan_enabled,
        zoom_enabled=zoom_enabled,
        boxselection_enabled=boxselection_enabled,
        auto_resize=auto_resize,
        key=key,
        default=None,
    )

    return component_value


# Helper functions for creating elements
def create_node(
    id: str,
    label: str,
    node_type: str,
    x: Optional[float] = None,
    y: Optional[float] = None,
    **additional_data
) -> Dict[str, Any]:
    """
    Helper function to create a node element

    Args:
        id: Unique node identifier
        label: Display label
        node_type: Node type (matches NodeStyle.type)
        x: Optional x-coordinate for fixed positioning
        y: Optional y-coordinate for fixed positioning
        **additional_data: Additional data properties

    Returns:
        Node element dictionary
    """
    node_data = {
        "id": id,
        "label": label,
        "type": node_type,
        **additional_data
    }

    node = {"data": node_data}

    # Add position if coordinates provided
    if x is not None and y is not None:
        node["position"] = {"x": x, "y": y}

    return node


def create_edge(
    id: str,
    source: str,
    target: str,
    edge_type: str,
    label: Optional[str] = None,
    **additional_data
) -> Dict[str, Any]:
    """
    Helper function to create an edge element

    Args:
        id: Unique edge identifier
        source: Source node ID
        target: Target node ID
        edge_type: Edge type (matches EdgeStyle.type)
        label: Optional edge label
        **additional_data: Additional data properties

    Returns:
        Edge element dictionary
    """
    edge_data = {
        "id": id,
        "source": source,
        "target": target,
        "type": edge_type,
        **additional_data
    }

    if label:
        edge_data["label"] = label

    return {"data": edge_data}
