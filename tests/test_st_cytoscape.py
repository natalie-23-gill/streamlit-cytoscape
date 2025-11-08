"""
Tests for the main st_cytoscape component function

Tests the st_cytoscape() function including element processing,
style handling, and position coordinate logic.
"""

import pytest
from unittest.mock import Mock, patch
from st_cytoscape.component import st_cytoscape
from st_cytoscape.styles import NodeStyle, EdgeStyle, HighlightStyle


class TestStCytoscapeFunction:
    """Tests for st_cytoscape() main function"""

    @patch('st_cytoscape.component._component_func')
    def test_st_cytoscape_basic(self, mock_component, sample_elements):
        """Test basic st_cytoscape call with minimal parameters"""
        mock_component.return_value = None

        result = st_cytoscape(elements=sample_elements)

        # Verify component was called
        mock_component.assert_called_once()
        call_kwargs = mock_component.call_args.kwargs

        # Check basic parameters
        assert len(call_kwargs['elements']) == 3
        assert call_kwargs['layout'] == 'cose'
        assert call_kwargs['height'] == 600
        assert call_kwargs['width'] == '100%'
        assert call_kwargs['selection_type'] == 'single'
        assert call_kwargs['enable_physics'] is True
        assert result is None

    @patch('st_cytoscape.component._component_func')
    def test_st_cytoscape_with_styles(
        self,
        mock_component,
        sample_elements,
        sample_node_style,
        sample_edge_style
    ):
        """Test st_cytoscape with node and edge styles"""
        mock_component.return_value = {"selected": ["n1"]}

        result = st_cytoscape(
            elements=sample_elements,
            node_styles=[sample_node_style],
            edge_styles=[sample_edge_style]
        )

        call_kwargs = mock_component.call_args.kwargs

        # Verify styles were converted to dicts
        assert len(call_kwargs['node_styles']) == 1
        assert call_kwargs['node_styles'][0]['type'] == 'person'
        assert call_kwargs['node_styles'][0]['color'] == '#3498db'

        assert len(call_kwargs['edge_styles']) == 1
        assert call_kwargs['edge_styles'][0]['type'] == 'knows'
        assert call_kwargs['edge_styles'][0]['color'] == '#95a5a6'

        assert result == {"selected": ["n1"]}

    @patch('st_cytoscape.component._component_func')
    def test_st_cytoscape_with_highlight_style(
        self,
        mock_component,
        sample_elements,
        sample_highlight_style
    ):
        """Test st_cytoscape with highlight style"""
        mock_component.return_value = None

        st_cytoscape(
            elements=sample_elements,
            highlight_style=sample_highlight_style
        )

        call_kwargs = mock_component.call_args.kwargs

        # Verify highlight style was converted
        assert call_kwargs['highlight_style'] is not None
        assert call_kwargs['highlight_style']['node_color'] == '#e74c3c'
        assert call_kwargs['highlight_style']['edge_color'] == '#e67e22'

    @patch('st_cytoscape.component._component_func')
    def test_st_cytoscape_without_highlight_style(
        self,
        mock_component,
        sample_elements
    ):
        """Test st_cytoscape without highlight style"""
        mock_component.return_value = None

        st_cytoscape(elements=sample_elements)

        call_kwargs = mock_component.call_args.kwargs
        assert call_kwargs['highlight_style'] is None

    @patch('st_cytoscape.component._component_func')
    def test_st_cytoscape_coordinate_positioning(self, mock_component):
        """Test element position processing from x,y coordinates (Issue #44)"""
        mock_component.return_value = None

        elements = [
            {
                "data": {
                    "id": "n1",
                    "label": "Node 1",
                    "type": "person",
                    "x": 100.0,
                    "y": 200.0
                }
            }
        ]

        st_cytoscape(elements=elements)

        call_kwargs = mock_component.call_args.kwargs
        processed_elements = call_kwargs['elements']

        # Verify position was added from x,y coordinates
        assert processed_elements[0]['position'] == {"x": 100.0, "y": 200.0}
        # Original data should still have x,y
        assert processed_elements[0]['data']['x'] == 100.0
        assert processed_elements[0]['data']['y'] == 200.0

    @patch('st_cytoscape.component._component_func')
    def test_st_cytoscape_position_from_node_style(self, mock_component):
        """Test element position from NodeStyle"""
        mock_component.return_value = None

        elements = [
            {"data": {"id": "n1", "label": "Node 1", "type": "person"}}
        ]

        node_style = NodeStyle(
            type="person",
            color="#3498db",
            position={"x": 150.0, "y": 250.0}
        )

        st_cytoscape(elements=elements, node_styles=[node_style])

        call_kwargs = mock_component.call_args.kwargs
        processed_elements = call_kwargs['elements']

        # Verify position was added from NodeStyle
        assert processed_elements[0]['position'] == {"x": 150.0, "y": 250.0}

    @patch('st_cytoscape.component._component_func')
    def test_st_cytoscape_existing_position_preserved(self, mock_component):
        """Test that existing position in element is preserved"""
        mock_component.return_value = None

        elements = [
            {
                "data": {"id": "n1", "label": "Node 1", "type": "person"},
                "position": {"x": 300.0, "y": 400.0}
            }
        ]

        st_cytoscape(elements=elements)

        call_kwargs = mock_component.call_args.kwargs
        processed_elements = call_kwargs['elements']

        # Verify existing position is preserved
        assert processed_elements[0]['position'] == {"x": 300.0, "y": 400.0}

    @patch('st_cytoscape.component._component_func')
    def test_st_cytoscape_custom_layout(self, mock_component, sample_elements):
        """Test st_cytoscape with custom layout"""
        mock_component.return_value = None

        st_cytoscape(elements=sample_elements, layout='grid')

        call_kwargs = mock_component.call_args.kwargs
        assert call_kwargs['layout'] == 'grid'

    @patch('st_cytoscape.component._component_func')
    def test_st_cytoscape_custom_dimensions(self, mock_component, sample_elements):
        """Test st_cytoscape with custom height and width"""
        mock_component.return_value = None

        st_cytoscape(
            elements=sample_elements,
            height=800,
            width="80%"
        )

        call_kwargs = mock_component.call_args.kwargs
        assert call_kwargs['height'] == 800
        assert call_kwargs['width'] == "80%"

    @patch('st_cytoscape.component._component_func')
    def test_st_cytoscape_selection_type(self, mock_component, sample_elements):
        """Test st_cytoscape with different selection types"""
        mock_component.return_value = None

        st_cytoscape(elements=sample_elements, selection_type='additive')

        call_kwargs = mock_component.call_args.kwargs
        assert call_kwargs['selection_type'] == 'additive'

    @patch('st_cytoscape.component._component_func')
    def test_st_cytoscape_interaction_options(self, mock_component, sample_elements):
        """Test st_cytoscape with interaction options"""
        mock_component.return_value = None

        st_cytoscape(
            elements=sample_elements,
            enable_physics=False,
            pan_enabled=False,
            zoom_enabled=False,
            boxselection_enabled=True
        )

        call_kwargs = mock_component.call_args.kwargs
        assert call_kwargs['enable_physics'] is False
        assert call_kwargs['pan_enabled'] is False
        assert call_kwargs['zoom_enabled'] is False
        assert call_kwargs['boxselection_enabled'] is True

    @patch('st_cytoscape.component._component_func')
    def test_st_cytoscape_auto_resize(self, mock_component, sample_elements):
        """Test st_cytoscape auto_resize option (Issue #35)"""
        mock_component.return_value = None

        st_cytoscape(elements=sample_elements, auto_resize=False)

        call_kwargs = mock_component.call_args.kwargs
        assert call_kwargs['auto_resize'] is False

    @patch('st_cytoscape.component._component_func')
    def test_st_cytoscape_with_key(self, mock_component, sample_elements):
        """Test st_cytoscape with custom key"""
        mock_component.return_value = None

        st_cytoscape(elements=sample_elements, key="my_graph")

        call_kwargs = mock_component.call_args.kwargs
        assert call_kwargs['key'] == "my_graph"

    @patch('st_cytoscape.component._component_func')
    def test_st_cytoscape_empty_styles(self, mock_component, sample_elements):
        """Test st_cytoscape with None styles"""
        mock_component.return_value = None

        st_cytoscape(
            elements=sample_elements,
            node_styles=None,
            edge_styles=None
        )

        call_kwargs = mock_component.call_args.kwargs
        assert call_kwargs['node_styles'] == []
        assert call_kwargs['edge_styles'] == []

    @patch('st_cytoscape.component._component_func')
    def test_st_cytoscape_elements_not_modified(self, mock_component):
        """Test that original elements list is not modified"""
        mock_component.return_value = None

        original_elements = [
            {
                "data": {
                    "id": "n1",
                    "label": "Node 1",
                    "type": "person",
                    "x": 100.0,
                    "y": 200.0
                }
            }
        ]

        # Make a copy to compare later
        import copy
        elements_copy = copy.deepcopy(original_elements)

        st_cytoscape(elements=original_elements)

        # Verify original elements were not modified
        assert original_elements == elements_copy
        # Original should not have position added
        assert 'position' not in original_elements[0]

    @patch('st_cytoscape.component._component_func')
    def test_st_cytoscape_edge_elements(self, mock_component):
        """Test that edge elements are processed correctly"""
        mock_component.return_value = None

        elements = [
            {"data": {"id": "n1", "label": "Node 1"}},
            {"data": {"id": "n2", "label": "Node 2"}},
            {
                "data": {
                    "id": "e1",
                    "source": "n1",
                    "target": "n2",
                    "type": "connects"
                }
            }
        ]

        st_cytoscape(elements=elements)

        call_kwargs = mock_component.call_args.kwargs
        processed_elements = call_kwargs['elements']

        # Verify edge was processed and has no position
        edge_elem = processed_elements[2]
        assert edge_elem['data']['source'] == 'n1'
        assert edge_elem['data']['target'] == 'n2'
        assert 'position' not in edge_elem

    @patch('st_cytoscape.component._component_func')
    def test_st_cytoscape_multiple_node_styles(self, mock_component):
        """Test st_cytoscape with multiple node styles"""
        mock_component.return_value = None

        elements = [
            {"data": {"id": "n1", "label": "Person", "type": "person"}},
            {"data": {"id": "n2", "label": "Company", "type": "company"}}
        ]

        styles = [
            NodeStyle(type="person", color="#3498db"),
            NodeStyle(type="company", color="#e74c3c")
        ]

        st_cytoscape(elements=elements, node_styles=styles)

        call_kwargs = mock_component.call_args.kwargs
        assert len(call_kwargs['node_styles']) == 2
        assert call_kwargs['node_styles'][0]['type'] == 'person'
        assert call_kwargs['node_styles'][1]['type'] == 'company'
