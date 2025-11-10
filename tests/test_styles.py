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
    style = NodeStyle("person", "#3498db", position={"x": 100, "y": 200})

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


class TestNodeStyleEdgeCases:
    """Edge case tests for NodeStyle"""

    def test_node_style_minimal(self):
        """Test NodeStyle with only required parameter"""
        style = NodeStyle("minimal")

        assert style.type == "minimal"
        assert style.color == "#666"  # Default value
        assert style.caption is None
        assert style.icon is None
        assert style.size == 40  # Default value

    def test_node_style_to_dict(self):
        """Test NodeStyle to_dict method includes all fields"""
        style = NodeStyle(
            "person", color="#3498db", caption="name", icon="user", size=60
        )

        result = style.to_dict()

        assert result["type"] == "person"
        assert result["color"] == "#3498db"
        assert result["caption"] == "name"
        assert result["icon"] == "user"
        assert result["size"] == 60

    def test_node_style_with_position_dict(self):
        """Test NodeStyle with position dictionary"""
        style = NodeStyle("person", position={"x": 150.0, "y": 250.0})

        style_dict = style.to_dict()
        assert style_dict["position"] == {"x": 150.0, "y": 250.0}

    def test_node_style_custom_styles_empty(self):
        """Test NodeStyle with empty custom_styles dict"""
        style = NodeStyle("person", custom_styles={})

        assert style.custom_styles == {}

    def test_node_style_custom_styles_override(self):
        """Test NodeStyle custom_styles can override base properties"""
        custom = {"background-color": "#000000", "border-width": 10}
        style = NodeStyle("person", color="#ffffff", custom_styles=custom)

        style_dict = style.to_dict()
        assert style_dict["color"] == "#ffffff"
        assert style_dict["custom_styles"]["background-color"] == "#000000"


class TestEdgeStyleEdgeCases:
    """Edge case tests for EdgeStyle"""

    def test_edge_style_minimal(self):
        """Test EdgeStyle with only required parameter"""
        style = EdgeStyle("minimal")

        assert style.type == "minimal"
        assert style.color == "#666"  # Default value
        assert style.caption is None
        assert style.directed is False  # Default value
        assert style.width == 2  # Default value

    def test_edge_style_to_dict(self):
        """Test EdgeStyle to_dict method includes all fields"""
        style = EdgeStyle(
            "knows", color="#95a5a6", caption="relationship", directed=False, width=2
        )

        result = style.to_dict()

        assert result["type"] == "knows"
        assert result["color"] == "#95a5a6"
        assert result["caption"] == "relationship"
        assert result["directed"] is False
        assert result["width"] == 2

    def test_edge_style_directed_false(self):
        """Test EdgeStyle with directed=False"""
        style = EdgeStyle("undirected", directed=False)

        assert style.directed is False

    def test_edge_style_directed_true(self):
        """Test EdgeStyle with directed=True"""
        style = EdgeStyle("directed", directed=True)

        assert style.directed is True

    def test_edge_style_custom_styles_complex(self):
        """Test EdgeStyle with complex custom_styles"""
        custom = {
            "curve-style": "bezier",
            "control-point-step-size": 40,
            "arrow-scale": 1.5,
        }
        style = EdgeStyle("complex", custom_styles=custom)

        style_dict = style.to_dict()
        assert style_dict["custom_styles"] == custom


class TestHighlightStyleEdgeCases:
    """Edge case tests for HighlightStyle"""

    def test_highlight_style_empty(self):
        """Test HighlightStyle with no parameters"""
        style = HighlightStyle()

        assert style.node_color is None
        assert style.edge_color is None
        assert style.node_border_color == "#FFD700"  # Default value
        assert style.node_border_width == 3  # Default value
        assert style.edge_width is None

    def test_highlight_style_to_dict_complete(self):
        """Test HighlightStyle to_dict with all parameters"""
        style = HighlightStyle(
            node_color="#FF0000",
            edge_color="#00FF00",
            node_border_color="#0000FF",
            node_border_width=5,
            edge_width=3,
        )

        result = style.to_dict()

        assert result["node_color"] == "#FF0000"
        assert result["edge_color"] == "#00FF00"
        assert result["node_border_color"] == "#0000FF"
        assert result["node_border_width"] == 5
        assert result["edge_width"] == 3

    def test_highlight_style_partial(self):
        """Test HighlightStyle with only some parameters"""
        style = HighlightStyle(node_color="#FF0000", edge_width=2)

        assert style.node_color == "#FF0000"
        assert style.edge_width == 2
        assert style.edge_color is None
        assert style.node_border_color == "#FFD700"  # Default value

    def test_highlight_style_zero_width(self):
        """Test HighlightStyle with zero width values"""
        style = HighlightStyle(node_border_width=0, edge_width=0)

        assert style.node_border_width == 0
        assert style.edge_width == 0
