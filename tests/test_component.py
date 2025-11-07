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
