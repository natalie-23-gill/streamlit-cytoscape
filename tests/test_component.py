"""
Tests for component helper functions
"""

import pytest
from st_cytoscape.component import create_node, create_edge


def test_create_node_basic():
    """Test basic node creation"""
    node = create_node("n1", "Node 1", "person")

    assert node["data"]["id"] == "n1"
    assert node["data"]["label"] == "Node 1"
    assert node["data"]["type"] == "person"
    assert "position" not in node


def test_create_node_with_position():
    """Test node creation with coordinates (Issue #44)"""
    node = create_node("n1", "Node 1", "person", x=100, y=200)

    assert node["position"] == {"x": 100, "y": 200}


def test_create_node_with_additional_data():
    """Test node creation with additional data"""
    node = create_node("n1", "Node 1", "person", age=30, city="NYC")

    assert node["data"]["age"] == 30
    assert node["data"]["city"] == "NYC"


def test_create_edge_basic():
    """Test basic edge creation"""
    edge = create_edge("e1", "n1", "n2", "knows")

    assert edge["data"]["id"] == "e1"
    assert edge["data"]["source"] == "n1"
    assert edge["data"]["target"] == "n2"
    assert edge["data"]["type"] == "knows"


def test_create_edge_with_label():
    """Test edge creation with label"""
    edge = create_edge("e1", "n1", "n2", "knows", label="friend")

    assert edge["data"]["label"] == "friend"


def test_create_edge_with_additional_data():
    """Test edge creation with additional data"""
    edge = create_edge("e1", "n1", "n2", "knows", weight=0.8)

    assert edge["data"]["weight"] == 0.8


class TestCreateNodeEdgeCases:
    """Edge case tests for create_node"""

    def test_create_node_with_zero_coordinates(self):
        """Test node creation with zero coordinates"""
        node = create_node("n1", "Node 1", "person", x=0, y=0)

        # Zero is a valid coordinate
        assert node["position"] == {"x": 0, "y": 0}

    def test_create_node_with_negative_coordinates(self):
        """Test node creation with negative coordinates"""
        node = create_node("n1", "Node 1", "person", x=-100, y=-200)

        assert node["position"] == {"x": -100, "y": -200}

    def test_create_node_with_float_coordinates(self):
        """Test node creation with float coordinates"""
        node = create_node("n1", "Node 1", "person", x=100.5, y=200.75)

        assert node["position"] == {"x": 100.5, "y": 200.75}

    def test_create_node_empty_label(self):
        """Test node creation with empty label"""
        node = create_node("n1", "", "person")

        assert node["data"]["label"] == ""
        assert node["data"]["id"] == "n1"

    def test_create_node_special_characters_in_label(self):
        """Test node creation with special characters in label"""
        node = create_node("n1", "Node <1> & 'Test'", "person")

        assert node["data"]["label"] == "Node <1> & 'Test'"

    def test_create_node_with_complex_additional_data(self):
        """Test node creation with complex additional data types"""
        node = create_node(
            "n1",
            "Node 1",
            "person",
            metadata={"key": "value"},
            tags=["tag1", "tag2"],
            count=42
        )

        assert node["data"]["metadata"] == {"key": "value"}
        assert node["data"]["tags"] == ["tag1", "tag2"]
        assert node["data"]["count"] == 42


class TestCreateEdgeEdgeCases:
    """Edge case tests for create_edge"""

    def test_create_edge_same_source_target(self):
        """Test edge creation with same source and target (self-loop)"""
        edge = create_edge("e1", "n1", "n1", "self_ref")

        assert edge["data"]["source"] == "n1"
        assert edge["data"]["target"] == "n1"

    def test_create_edge_empty_string_label(self):
        """Test edge creation with empty string label"""
        edge = create_edge("e1", "n1", "n2", "knows", label="")

        # Empty string is falsy, so label is not added
        assert "label" not in edge["data"]

    def test_create_edge_none_label(self):
        """Test edge creation with None label (should not be added)"""
        edge = create_edge("e1", "n1", "n2", "knows", label=None)

        # None label should not add label to data
        assert "label" not in edge["data"]

    def test_create_edge_with_label_and_additional_data(self):
        """Test edge creation with both label and additional data"""
        edge = create_edge(
            "e1",
            "n1",
            "n2",
            "knows",
            label="friend",
            weight=0.9,
            since=2020
        )

        assert edge["data"]["label"] == "friend"
        assert edge["data"]["weight"] == 0.9
        assert edge["data"]["since"] == 2020

    def test_create_edge_special_characters_in_ids(self):
        """Test edge creation with special characters in IDs"""
        edge = create_edge("e-1", "n_1", "n.2", "knows")

        assert edge["data"]["id"] == "e-1"
        assert edge["data"]["source"] == "n_1"
        assert edge["data"]["target"] == "n.2"
