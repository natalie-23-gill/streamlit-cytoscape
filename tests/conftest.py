"""
Shared pytest fixtures for st-cytoscape tests
"""

import pytest
from st_cytoscape.styles import NodeStyle, EdgeStyle, HighlightStyle


@pytest.fixture
def sample_node():
    """Basic node element for testing"""
    return {"data": {"id": "n1", "label": "Test Node", "type": "person"}}


@pytest.fixture
def sample_node_with_position():
    """Node element with position coordinates"""
    return {
        "data": {
            "id": "n2",
            "label": "Positioned Node",
            "type": "person",
            "x": 100.0,
            "y": 200.0,
        }
    }


@pytest.fixture
def sample_edge():
    """Basic edge element for testing"""
    return {"data": {"id": "e1", "source": "n1", "target": "n2", "type": "knows"}}


@pytest.fixture
def sample_elements(sample_node, sample_edge):
    """List of sample graph elements"""
    return [
        sample_node,
        {"data": {"id": "n2", "label": "Node 2", "type": "person"}},
        sample_edge,
    ]


@pytest.fixture
def sample_node_style():
    """Basic NodeStyle for testing"""
    return NodeStyle(type="person", color="#3498db", size=50)


@pytest.fixture
def sample_edge_style():
    """Basic EdgeStyle for testing"""
    return EdgeStyle(type="knows", color="#95a5a6", width=2)


@pytest.fixture
def sample_highlight_style():
    """Basic HighlightStyle for testing"""
    return HighlightStyle(
        node_color="#e74c3c", edge_color="#e67e22", node_border_width=3, edge_width=4
    )


@pytest.fixture
def sample_event_data():
    """Sample event data dictionary"""
    return {
        "type": "node_click",
        "target": {"id": "n1", "label": "Test Node"},
        "selected_nodes": ["n1"],
        "selected_edges": [],
    }
