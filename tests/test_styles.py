"""Integration tests for custom styles functionality."""

from playwright.sync_api import Page


PAGE_NAME = "Custom Styles"
NODE_ID = "n1"  # First PERSON node in social.json
EDGE_ID = "e1"  # First FOLLOWS edge in social.json
ASSIGN_CY = "const cy = document.getElementById('cy')._cyreg.cy;"
FRAME_LOCATOR = "iframe[title*='streamlit_cytoscape']"


def get_node_style(node_id, iframe):
    """Get the computed style of a node from Cytoscape.js."""
    style = iframe.evaluate(
        f"""() => {{
        {ASSIGN_CY}
        const node = cy.getElementById("{node_id}");
        if (!node || node.length === 0) return null;
        return {{
            'background-color': node.style('background-color'),
            'border-width': node.style('border-width'),
            'border-color': node.style('border-color'),
            'shape': node.style('shape'),
        }};
    }}"""
    )
    return style


def get_follows_edge_style(iframe):
    """Get the computed style of the first FOLLOWS edge."""
    style = iframe.evaluate(
        f"""() => {{
        {ASSIGN_CY}
        const edges = cy.edges('[label="FOLLOWS"]');
        if (edges.length > 0) {{
            const edge = edges[0];
            return {{
                'line-style': edge.style('line-style'),
                'width': edge.style('width'),
            }};
        }}
        return null;
    }}"""
    )
    return style


def test_iframe_exists_custom_styles(page: Page):
    """Test that custom styles page loads with iframe."""
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")
    page.wait_for_selector(FRAME_LOCATOR, timeout=10000)
    frames = page.query_selector_all(FRAME_LOCATOR)
    assert len(frames) == 1


def test_node_custom_border_style(page: Page):
    """Test that node custom border styles are applied."""
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")
    page.wait_for_selector(FRAME_LOCATOR, timeout=10000)
    frame = page.frame_locator(FRAME_LOCATOR).first.locator(":root")
    frame.click(position={"x": 0, "y": 0})  # await and scroll to view

    # Get a PERSON node (they have custom styles applied)
    style = get_node_style(NODE_ID, frame)

    assert style is not None, f"Node {NODE_ID} not found"
    # Default border-width is 3 in the demo
    assert style["border-width"] == "3px"


def test_node_shape_default(page: Page):
    """Test that node shape defaults to ellipse."""
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")
    page.wait_for_selector(FRAME_LOCATOR, timeout=10000)
    frame = page.frame_locator(FRAME_LOCATOR).first.locator(":root")
    frame.click(position={"x": 0, "y": 0})  # await and scroll to view

    # Get initial shape (default is ellipse)
    style = get_node_style(NODE_ID, frame)
    assert style is not None, f"Node {NODE_ID} not found"
    assert style["shape"] == "ellipse"


def test_edge_custom_line_style(page: Page):
    """Test that edge custom line styles are applied."""
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")
    page.wait_for_selector(FRAME_LOCATOR, timeout=10000)
    frame = page.frame_locator(FRAME_LOCATOR).first.locator(":root")
    frame.click(position={"x": 0, "y": 0})  # await and scroll to view

    edge_style = get_follows_edge_style(frame)

    # Default line-style is solid in the demo
    assert edge_style is not None, "No FOLLOWS edge found"
    assert edge_style["line-style"] == "solid"


def test_edge_custom_width(page: Page):
    """Test that edge custom width is applied."""
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")
    page.wait_for_selector(FRAME_LOCATOR, timeout=10000)
    frame = page.frame_locator(FRAME_LOCATOR).first.locator(":root")
    frame.click(position={"x": 0, "y": 0})  # await and scroll to view

    edge_style = get_follows_edge_style(frame)

    # Default width is 2 in the demo
    assert edge_style is not None, "No FOLLOWS edge found"
    assert edge_style["width"] == "2px"
