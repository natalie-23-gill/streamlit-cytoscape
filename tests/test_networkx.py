from playwright.sync_api import Page


PAGE_NAME = "NetworkX"
FRAME_LOCATOR = "iframe[title*='streamlit_cytoscape']"
ASSIGN_CY = "const cy = document.getElementById('cy')._cyreg.cy;"


def test_networkx_elements_render(page: Page):
    """nx.cytoscape_data() output produces a valid graph."""
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")
    page.wait_for_selector(FRAME_LOCATOR, timeout=10000)

    frame = page.frame_locator(FRAME_LOCATOR).first.locator(":root")

    result = frame.evaluate(
        f"""() => {{
        {ASSIGN_CY}
        return {{
            nodes: cy.nodes().length,
            edges: cy.edges().length,
        }};
    }}"""
    )

    # nx.karate_club_graph() produces 34 nodes and 78 edges
    assert result["nodes"] == 34
    assert result["edges"] == 78


def test_networkx_edge_connectivity(page: Page):
    """Edges connect to nodes after int/str coercion."""
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")
    page.wait_for_selector(FRAME_LOCATOR, timeout=10000)

    frame = page.frame_locator(FRAME_LOCATOR).first.locator(":root")

    result = frame.evaluate(
        f"""() => {{
        {ASSIGN_CY}
        const orphaned = cy.edges().filter(e =>
            e.source().length === 0 || e.target().length === 0
        );
        return orphaned.length;
    }}"""
    )

    assert result == 0
