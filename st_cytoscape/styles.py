"""
Style classes for nodes, edges, and highlights in st-cytoscape
"""

from typing import Optional, Dict, Any, Union


class NodeStyle:
    """
    Defines the visual style for graph nodes.

    Addresses Issue #44: Supports coordinate-based positioning
    Addresses PR #62: Built-in custom_styles support

    Args:
        type: Node type identifier
        color: Node color (hex or color name)
        caption: Property to display as node label
        icon: Material icon name
        size: Node size in pixels
        position: Optional dict with 'x' and 'y' coordinates for fixed positioning
        custom_styles: Additional cytoscape.js style properties
    """

    def __init__(
        self,
        type: str,
        color: str = "#666",
        caption: Optional[str] = None,
        icon: Optional[str] = None,
        size: int = 40,
        position: Optional[Dict[str, float]] = None,
        custom_styles: Optional[Dict[str, Any]] = None
    ):
        self.type = type
        self.color = color
        self.caption = caption
        self.icon = icon
        self.size = size
        self.position = position
        self.custom_styles = custom_styles or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "type": self.type,
            "color": self.color,
            "caption": self.caption,
            "icon": self.icon,
            "size": self.size,
            "position": self.position,
            "custom_styles": self.custom_styles,
        }


class EdgeStyle:
    """
    Defines the visual style for graph edges.

    Addresses PR #62: Built-in custom_styles support

    Args:
        type: Edge type identifier
        color: Edge color (hex or color name)
        caption: Property to display as edge label
        directed: Whether to show directional arrow
        width: Edge width in pixels
        custom_styles: Additional cytoscape.js style properties (e.g., line-style, curve-style)
    """

    def __init__(
        self,
        type: str,
        color: str = "#666",
        caption: Optional[str] = None,
        directed: bool = False,
        width: int = 2,
        custom_styles: Optional[Dict[str, Any]] = None
    ):
        self.type = type
        self.color = color
        self.caption = caption
        self.directed = directed
        self.width = width
        self.custom_styles = custom_styles or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "type": self.type,
            "color": self.color,
            "caption": self.caption,
            "directed": self.directed,
            "width": self.width,
            "custom_styles": self.custom_styles,
        }


class HighlightStyle:
    """
    Defines the visual style for highlighted elements.

    Addresses Issue #63: Customizable highlight styles

    Args:
        node_color: Color for highlighted nodes
        node_border_width: Border width for highlighted nodes
        node_border_color: Border color for highlighted nodes
        edge_color: Color for highlighted edges
        edge_width: Width for highlighted edges
        custom_styles: Additional cytoscape.js style properties for highlights
    """

    def __init__(
        self,
        node_color: Optional[str] = None,
        node_border_width: int = 3,
        node_border_color: str = "#FFD700",
        edge_color: Optional[str] = None,
        edge_width: Optional[int] = None,
        custom_styles: Optional[Dict[str, Any]] = None
    ):
        self.node_color = node_color
        self.node_border_width = node_border_width
        self.node_border_color = node_border_color
        self.edge_color = edge_color
        self.edge_width = edge_width
        self.custom_styles = custom_styles or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "node_color": self.node_color,
            "node_border_width": self.node_border_width,
            "node_border_color": self.node_border_color,
            "edge_color": self.edge_color,
            "edge_width": self.edge_width,
            "custom_styles": self.custom_styles,
        }
