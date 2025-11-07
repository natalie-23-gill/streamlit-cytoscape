"""
Tests for style classes
"""

import pytest
from st_cytoscape.styles import NodeStyle, EdgeStyle, HighlightStyle


def test_node_style_basic():
    """Test basic NodeStyle creation"""
    style = NodeStyle("person", "#3498db", "name", "person", size=50)

    assert style.type == "person"
    assert style.color == "#3498db"
    assert style.caption == "name"
    assert style.icon == "person"
    assert style.size == 50
    assert style.position is None
    assert style.custom_styles == {}


def test_node_style_with_position():
    """Test NodeStyle with coordinate positioning (Issue #44)"""
    style = NodeStyle(
        "person",
        "#3498db",
        position={"x": 100, "y": 200}
    )

    style_dict = style.to_dict()
    assert style_dict["position"] == {"x": 100, "y": 200}


def test_node_style_with_custom_styles():
    """Test NodeStyle with custom_styles (PR #62)"""
    custom = {
        "shape": "diamond",
        "border-width": 5,
    }
    style = NodeStyle("custom", "#9b59b6", custom_styles=custom)

    style_dict = style.to_dict()
    assert style_dict["custom_styles"] == custom


def test_edge_style_basic():
    """Test basic EdgeStyle creation"""
    style = EdgeStyle("knows", "#95a5a6", "label", directed=True, width=3)

    assert style.type == "knows"
    assert style.color == "#95a5a6"
    assert style.caption == "label"
    assert style.directed is True
    assert style.width == 3
    assert style.custom_styles == {}


def test_edge_style_with_custom_styles():
    """Test EdgeStyle with custom_styles (PR #62)"""
    custom = {
        "line-style": "dashed",
        "curve-style": "bezier",
    }
    style = EdgeStyle("special", custom_styles=custom)

    style_dict = style.to_dict()
    assert style_dict["custom_styles"] == custom


def test_highlight_style():
    """Test HighlightStyle (Issue #63)"""
    style = HighlightStyle(
        node_border_color="#FFD700",
        node_border_width=4,
        edge_color="#FF6347",
        edge_width=5,
    )

    style_dict = style.to_dict()
    assert style_dict["node_border_color"] == "#FFD700"
    assert style_dict["node_border_width"] == 4
    assert style_dict["edge_color"] == "#FF6347"
    assert style_dict["edge_width"] == 5


def test_highlight_style_with_custom_styles():
    """Test HighlightStyle with custom_styles"""
    custom = {"background-opacity": 1.0}
    style = HighlightStyle(custom_styles=custom)

    style_dict = style.to_dict()
    assert style_dict["custom_styles"] == custom
