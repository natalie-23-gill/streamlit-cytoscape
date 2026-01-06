from playwright.sync_api import Page
import json
import re


PAGE_NAME = "Edge Actions"
ASSIGN_CY = "const cy = document.getElementById('cy')._cyreg.cy;"
FRAME_LOCATOR = "iframe[title*='streamlit_cytoscape']"


def AWAIT_RETURN_ACTION(page):
    page.get_by_text('"action":"').click(timeout=10000)


def get_edge_count(iframe):
    """Get the count of visible edges"""
    count = iframe.evaluate(
        f"""() => {{
        {ASSIGN_CY}
        return cy.edges().length;
    }}"""
    )
    return count


def get_meta_edge_count(iframe):
    """Get the count of meta-edges"""
    count = iframe.evaluate(
        f"""() => {{
        {ASSIGN_CY}
        return cy.edges('[_isMetaEdge]').length;
    }}"""
    )
    return count


def get_meta_edge_pos(iframe):
    """Get the position of the first meta-edge"""
    pos = iframe.evaluate(
        f"""() => {{
        {ASSIGN_CY}
        const metaEdge = cy.edges('[_isMetaEdge]').first();
        if (!metaEdge || metaEdge.length === 0) return null;
        const sourcePos = metaEdge.source().renderedPosition();
        const targetPos = metaEdge.target().renderedPosition();
        return {{
            x: (sourcePos.x + targetPos.x) / 2,
            y: (sourcePos.y + targetPos.y) / 2
        }};
    }}"""
    )
    return pos


def get_meta_edge_label(iframe):
    """Get the label of the first meta-edge"""
    label = iframe.evaluate(
        f"""() => {{
        {ASSIGN_CY}
        const metaEdge = cy.edges('[_isMetaEdge]').first();
        return metaEdge ? metaEdge.data('_metaLabel') : null;
    }}"""
    )
    return label


def get_return_json(page: Page):
    AWAIT_RETURN_ACTION(page)
    data = (
        page.get_by_test_id("stJson")
        .first.text_content()
        .replace('""', '","')
        .replace('}"', '},"')
    )
    data = re.sub("([0-9]+):", "", data)
    return json.loads(data)


def test_iframe_exists_edge_actions(page: Page):
    """Test that the iframe exists on the Edge Actions page"""
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")
    frames = page.query_selector_all(FRAME_LOCATOR)
    assert len(frames) == 1


def test_auto_collapse_on_render(page: Page):
    """Test that parallel edges are collapsed on initial render"""
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")
    frame = page.frame_locator(FRAME_LOCATOR).first.locator(":root")
    frame.click(position={"x": 0, "y": 0})  # await and scroll to view

    # Wait for collapse to complete
    page.wait_for_timeout(500)

    # Should have meta-edges (3 groups of parallel edges in test data)
    meta_count = get_meta_edge_count(frame)
    assert meta_count > 0, "Expected at least one meta-edge"


def test_expand_edge_dblclick(page: Page):
    """Test that double-clicking a collapsed edge expands it"""
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")
    frame = page.frame_locator(FRAME_LOCATOR).first.locator(":root")
    frame.click(position={"x": 0, "y": 0})  # await and scroll to view

    # Wait for collapse to complete
    page.wait_for_timeout(500)

    # Get initial counts
    initial_meta_count = get_meta_edge_count(frame)
    initial_edge_count = get_edge_count(frame)

    # Double-click on meta-edge
    pos = get_meta_edge_pos(frame)
    assert pos is not None, "No meta-edge found to click"
    frame.dblclick(position=pos)

    # Wait for expand
    page.wait_for_timeout(300)

    # Check that meta-edge count decreased
    new_meta_count = get_meta_edge_count(frame)
    new_edge_count = get_edge_count(frame)

    assert (
        new_meta_count < initial_meta_count
    ), "Meta-edge should be removed after expand"
    assert (
        new_edge_count > initial_edge_count
    ), "Edge count should increase after expand"


def test_expand_edge_returns_data(page: Page):
    """Test that expanding returns proper data structure"""
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")
    frame = page.frame_locator(FRAME_LOCATOR).first.locator(":root")
    frame.click(position={"x": 0, "y": 0})  # await and scroll to view

    # Wait for collapse to complete
    page.wait_for_timeout(500)

    # Double-click on meta-edge
    pos = get_meta_edge_pos(frame)
    assert pos is not None, "No meta-edge found to click"
    frame.dblclick(position=pos)

    # Get returned data
    data = get_return_json(page)

    assert data["action"] == "expand_edge"
    assert "group_key" in data["data"]
    assert "edge_count" in data["data"]
    assert data["data"]["edge_count"] >= 2


def test_priority_label_display(page: Page):
    """Test that priority label is shown on meta-edge"""
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")
    frame = page.frame_locator(FRAME_LOCATOR).first.locator(":root")
    frame.click(position={"x": 0, "y": 0})  # await and scroll to view

    # Wait for collapse to complete
    page.wait_for_timeout(500)

    # Verify meta-edge has expected label structure
    label = get_meta_edge_label(frame)

    assert label is not None, "Meta-edge should have a label"
    assert "(" in label and ")" in label, "Label should have count"


def test_single_edges_not_collapsed(page: Page):
    """Test that single edges (non-parallel) are not collapsed"""
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")
    frame = page.frame_locator(FRAME_LOCATOR).first.locator(":root")
    frame.click(position={"x": 0, "y": 0})  # await and scroll to view

    # Wait for collapse to complete
    page.wait_for_timeout(500)

    # Check that we have both meta-edges and regular edges
    # Our test data has 8 edges: 3 parallel groups + 1 single edge
    # After collapse: 3 meta-edges + 1 regular edge = 4 edges
    total_edges = get_edge_count(frame)
    meta_edges = get_meta_edge_count(frame)

    # There should be at least one non-meta edge (charlie->diana)
    non_meta_edges = total_edges - meta_edges
    assert non_meta_edges >= 1, "Single edges should not be collapsed"


def test_meta_edge_label_includes_count(page: Page):
    """Test that meta-edge label includes edge count in parentheses"""
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")
    frame = page.frame_locator(FRAME_LOCATOR).first.locator(":root")
    frame.click(position={"x": 0, "y": 0})  # await and scroll to view

    # Wait for collapse to complete
    page.wait_for_timeout(500)

    # Get all meta-edge labels
    labels = frame.evaluate(
        f"""() => {{
        {ASSIGN_CY}
        return cy.edges('[_isMetaEdge]').map(e => ({{
            label: e.data('_metaLabel'),
            count: e.data('_edgeCount')
        }}));
    }}"""
    )

    assert len(labels) > 0, "Expected at least one meta-edge"

    for edge_info in labels:
        label = edge_info["label"]
        count = edge_info["count"]
        # Label should contain the count in parentheses
        assert f"({count})" in label, (
            f"Meta-edge label should include count. "
            f"Expected '({count})' in '{label}'"
        )


def test_meta_edge_rendered_label_matches_meta_label(page: Page):
    """Test that the rendered label on meta-edges uses _metaLabel."""
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")
    frame = page.frame_locator(FRAME_LOCATOR).first.locator(":root")
    frame.click(position={"x": 0, "y": 0})  # await and scroll to view

    # Wait for collapse to complete
    page.wait_for_timeout(500)

    # Check that the rendered label matches _metaLabel (with count)
    # not just the label field (without count)
    result = frame.evaluate(
        f"""() => {{
        {ASSIGN_CY}
        const metaEdge = cy.edges('[_isMetaEdge]').first();
        if (!metaEdge || metaEdge.length === 0) return null;
        return {{
            renderedLabel: metaEdge.style('label'),
            metaLabel: metaEdge.data('_metaLabel'),
            labelField: metaEdge.data('label')
        }};
    }}"""
    )

    assert result is not None, "No meta-edge found"
    # The rendered label should match _metaLabel (which includes count)
    # not the label field (which doesn't include count)
    assert result["renderedLabel"] == result["metaLabel"], (
        f"Rendered label '{result['renderedLabel']}' should match "
        f"_metaLabel '{result['metaLabel']}', "
        f"not label '{result['labelField']}'"
    )
