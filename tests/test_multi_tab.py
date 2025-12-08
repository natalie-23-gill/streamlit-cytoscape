"""
Tests for multi-tab auto-fit functionality (st-link-analysis#35).

Verifies that graphs in hidden tabs auto-fit when the tab becomes visible.
"""

from playwright.sync_api import Page, expect


PAGE_NAME = "Multi-Tab"
FRAME_LOCATOR = "iframe[title*='streamlit_cytoscape']"
ASSIGN_CY = "const cy = document.getElementById('cy')._cyreg.cy;"


def get_graph_extent(frame):
    """Get the rendered extent (bounding box) of all elements in the graph."""
    return frame.evaluate(
        f"""() => {{
        {ASSIGN_CY}
        return cy.extent();
    }}"""
    )


def get_container_dimensions(frame):
    """Get the dimensions of the cytoscape container."""
    return frame.evaluate(
        """() => {
        const container = document.getElementById('cy');
        return {
            width: container.clientWidth,
            height: container.clientHeight
        };
    }"""
    )


def get_elements_count(frame):
    """Get the number of nodes and edges in the graph."""
    return frame.evaluate(
        f"""() => {{
        {ASSIGN_CY}
        return {{
            nodes: cy.nodes().length,
            edges: cy.edges().length
        }};
    }}"""
    )


def test_multi_tab_page_exists(page: Page):
    """Test that the Multi-Tab demo page exists and loads."""
    page.get_by_role("link", name=PAGE_NAME).click()
    expect(page).to_have_title(PAGE_NAME)


def test_tab1_graph_renders(page: Page):
    """Test that the graph in Tab 1 renders correctly on page load."""
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")
    page.wait_for_selector(FRAME_LOCATOR, timeout=10000)

    frames = page.query_selector_all(FRAME_LOCATOR)
    assert len(frames) >= 1, "Expected at least one iframe for Tab 1"

    frame = page.frame_locator(FRAME_LOCATOR).first.locator(":root")
    frame.click(position={"x": 0, "y": 0})  # scroll into view

    # Verify graph has elements
    counts = get_elements_count(frame)
    assert counts["nodes"] > 0, "Tab 1 graph should have nodes"
    assert counts["edges"] > 0, "Tab 1 graph should have edges"

    # Verify container has dimensions
    dims = get_container_dimensions(frame)
    assert dims["width"] > 0, "Container should have width"
    assert dims["height"] > 0, "Container should have height"


def test_tab2_graph_auto_fits_on_visibility(page: Page):
    """Test that the graph in Tab 2 auto-fits when the tab becomes visible."""
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")
    page.wait_for_selector(FRAME_LOCATOR, timeout=10000)

    # Click on Tab 2 to switch tabs
    page.get_by_role("tab", name="Tab 2").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(500)  # Allow time for ResizeObserver to trigger

    # Tab 2's iframe is the second one (nth(1)) - Tab 1's iframe gets hidden
    frame = page.frame_locator(FRAME_LOCATOR).nth(1)

    # Verify graph has elements (different graph than Tab 1 - 6 nodes vs 5)
    counts = frame.locator(":root").evaluate(
        f"""() => {{
        {ASSIGN_CY}
        return {{
            nodes: cy.nodes().length,
            edges: cy.edges().length
        }};
    }}"""
    )
    assert counts["nodes"] == 6, "Tab 2 graph should have 6 nodes"
    assert counts["edges"] == 6, "Tab 2 graph should have 6 edges"

    # Verify container has valid dimensions (not zero - which was the bug)
    dims = frame.locator(":root").evaluate(
        """() => {
        const container = document.getElementById('cy');
        return {
            width: container.clientWidth,
            height: container.clientHeight
        };
    }"""
    )
    assert dims["width"] > 0, "Tab 2 container should have width after becoming visible"
    assert (
        dims["height"] > 0
    ), "Tab 2 container should have height after becoming visible"

    # Verify graph extent is within reasonable bounds of the container
    # This confirms the graph was fitted after the tab became visible
    extent = frame.locator(":root").evaluate(
        f"""() => {{
        {ASSIGN_CY}
        return cy.extent();
    }}"""
    )
    assert extent["w"] > 0, "Graph extent width should be positive"
    assert extent["h"] > 0, "Graph extent height should be positive"


def test_switch_back_to_tab1(page: Page):
    """Test that switching back to Tab 1 still shows the graph correctly."""
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")
    page.wait_for_selector(FRAME_LOCATOR, timeout=10000)

    # Switch to Tab 2 then back to Tab 1
    page.get_by_role("tab", name="Tab 2").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(500)

    page.get_by_role("tab", name="Tab 1").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_selector(FRAME_LOCATOR, state="visible", timeout=10000)
    page.wait_for_timeout(500)

    frame = page.frame_locator(FRAME_LOCATOR).first

    # Verify Tab 1 graph still renders correctly (5 nodes vs Tab 2's 6)
    counts = frame.locator(":root").evaluate(
        f"""() => {{
        {ASSIGN_CY}
        return {{
            nodes: cy.nodes().length,
            edges: cy.edges().length
        }};
    }}"""
    )
    assert counts["nodes"] == 5, "Tab 1 graph should have 5 nodes after switching back"

    dims = frame.locator(":root").evaluate(
        """() => {
        const container = document.getElementById('cy');
        return {
            width: container.clientWidth,
            height: container.clientHeight
        };
    }"""
    )
    assert dims["width"] > 0, "Tab 1 container should still have width"
    assert dims["height"] > 0, "Tab 1 container should still have height"
