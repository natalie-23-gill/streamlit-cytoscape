"""
Event handling for st-cytoscape interactions
"""

from typing import Optional, Dict, Any, List
from enum import Enum


class EventType(Enum):
    """Types of events that can occur in the graph"""
    NODE_CLICK = "node_click"
    EDGE_CLICK = "edge_click"
    NODE_DOUBLE_CLICK = "node_double_click"
    NODE_HOVER = "node_hover"
    EDGE_HOVER = "edge_hover"
    BACKGROUND_CLICK = "background_click"
    SELECTION_CHANGE = "selection_change"


class Event:
    """
    Represents an interaction event from the graph component.

    Attributes:
        type: The type of event that occurred
        target: The element that triggered the event (node or edge data)
        selected_nodes: List of currently selected node IDs
        selected_edges: List of currently selected edge IDs
    """

    def __init__(
        self,
        event_type: str,
        target: Optional[Dict[str, Any]] = None,
        selected_nodes: Optional[List[str]] = None,
        selected_edges: Optional[List[str]] = None
    ):
        self.type = event_type
        self.target = target or {}
        self.selected_nodes = selected_nodes or []
        self.selected_edges = selected_edges or []

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Event":
        """Create an Event from a dictionary"""
        return cls(
            event_type=data.get("type", ""),
            target=data.get("target"),
            selected_nodes=data.get("selected_nodes"),
            selected_edges=data.get("selected_edges"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "type": self.type,
            "target": self.target,
            "selected_nodes": self.selected_nodes,
            "selected_edges": self.selected_edges,
        }
