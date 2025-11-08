"""
Tests for st_cytoscape.events module

Tests the Event class and EventType enum for handling graph interactions.
"""

import pytest
from st_cytoscape.events import Event, EventType


class TestEventType:
    """Tests for EventType enum"""

    def test_event_type_values(self):
        """Test that all event types have correct string values"""
        assert EventType.NODE_CLICK.value == "node_click"
        assert EventType.EDGE_CLICK.value == "edge_click"
        assert EventType.NODE_DOUBLE_CLICK.value == "node_double_click"
        assert EventType.NODE_HOVER.value == "node_hover"
        assert EventType.EDGE_HOVER.value == "edge_hover"
        assert EventType.BACKGROUND_CLICK.value == "background_click"
        assert EventType.SELECTION_CHANGE.value == "selection_change"

    def test_event_type_count(self):
        """Test that we have all expected event types"""
        # Ensure we have exactly 7 event types defined
        assert len(EventType) == 7


class TestEvent:
    """Tests for Event class"""

    def test_event_init_basic(self):
        """Test basic Event initialization"""
        event = Event(event_type="node_click")

        assert event.type == "node_click"
        assert event.target == {}
        assert event.selected_nodes == []
        assert event.selected_edges == []

    def test_event_init_with_target(self):
        """Test Event initialization with target data"""
        target_data = {"id": "n1", "label": "Node 1", "type": "person"}
        event = Event(event_type="node_click", target=target_data)

        assert event.type == "node_click"
        assert event.target == target_data
        assert event.selected_nodes == []
        assert event.selected_edges == []

    def test_event_init_with_selected_nodes(self):
        """Test Event initialization with selected nodes"""
        selected = ["n1", "n2", "n3"]
        event = Event(
            event_type="selection_change",
            selected_nodes=selected
        )

        assert event.type == "selection_change"
        assert event.selected_nodes == selected
        assert event.selected_edges == []

    def test_event_init_with_selected_edges(self):
        """Test Event initialization with selected edges"""
        selected = ["e1", "e2"]
        event = Event(
            event_type="selection_change",
            selected_edges=selected
        )

        assert event.type == "selection_change"
        assert event.selected_nodes == []
        assert event.selected_edges == selected

    def test_event_init_complete(self):
        """Test Event initialization with all parameters"""
        target_data = {"id": "e1", "source": "n1", "target": "n2"}
        event = Event(
            event_type="edge_click",
            target=target_data,
            selected_nodes=["n1", "n2"],
            selected_edges=["e1"]
        )

        assert event.type == "edge_click"
        assert event.target == target_data
        assert event.selected_nodes == ["n1", "n2"]
        assert event.selected_edges == ["e1"]

    def test_event_from_dict_basic(self, sample_event_data):
        """Test creating Event from dictionary"""
        event = Event.from_dict(sample_event_data)

        assert event.type == "node_click"
        assert event.target == {"id": "n1", "label": "Test Node"}
        assert event.selected_nodes == ["n1"]
        assert event.selected_edges == []

    def test_event_from_dict_empty(self):
        """Test creating Event from empty dictionary"""
        event = Event.from_dict({})

        assert event.type == ""
        # When None is passed to __init__, it defaults to {} or []
        assert event.target == {}
        assert event.selected_nodes == []
        assert event.selected_edges == []

    def test_event_from_dict_partial(self):
        """Test creating Event from partial dictionary"""
        data = {
            "type": "background_click",
            "selected_nodes": []
        }
        event = Event.from_dict(data)

        assert event.type == "background_click"
        # When None is passed to __init__, it defaults to {}
        assert event.target == {}
        assert event.selected_nodes == []
        # When None is passed to __init__, it defaults to []
        assert event.selected_edges == []

    def test_event_to_dict(self):
        """Test converting Event to dictionary"""
        event = Event(
            event_type="node_hover",
            target={"id": "n5", "label": "Hovered"},
            selected_nodes=["n5"],
            selected_edges=[]
        )

        result = event.to_dict()

        assert result == {
            "type": "node_hover",
            "target": {"id": "n5", "label": "Hovered"},
            "selected_nodes": ["n5"],
            "selected_edges": []
        }

    def test_event_to_dict_defaults(self):
        """Test converting Event with defaults to dictionary"""
        event = Event(event_type="background_click")

        result = event.to_dict()

        assert result == {
            "type": "background_click",
            "target": {},
            "selected_nodes": [],
            "selected_edges": []
        }

    def test_event_roundtrip(self, sample_event_data):
        """Test Event can roundtrip through dict conversion"""
        original = Event.from_dict(sample_event_data)
        converted = original.to_dict()
        restored = Event.from_dict(converted)

        assert restored.type == original.type
        assert restored.target == original.target
        assert restored.selected_nodes == original.selected_nodes
        assert restored.selected_edges == original.selected_edges

    def test_event_with_event_type_enum(self):
        """Test Event works with EventType enum values"""
        event = Event(event_type=EventType.NODE_DOUBLE_CLICK.value)

        assert event.type == "node_double_click"

    def test_event_multiple_selections(self):
        """Test Event with multiple selected nodes and edges"""
        event = Event(
            event_type="selection_change",
            selected_nodes=["n1", "n2", "n3", "n4"],
            selected_edges=["e1", "e2", "e3"]
        )

        assert len(event.selected_nodes) == 4
        assert len(event.selected_edges) == 3
        assert "n3" in event.selected_nodes
        assert "e2" in event.selected_edges
