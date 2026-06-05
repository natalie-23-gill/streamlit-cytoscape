from playwright.sync_api import Page, expect

PAGE_NAME = "Links & Updates"
FRAME_LOCATOR = "iframe[title*='streamlit_cytoscape']"
ASSIGN_CY = "const cy = document.getElementById('cy')._cyreg.cy;"


def wait_for_node(_id, frame):
    """Wait for a node to exist in the Cytoscape graph."""
    frame.evaluate(f"""() => {{
        {ASSIGN_CY}
        return new Promise((resolve) => {{
            const check = () => {{
                const node = cy.getElementById("{_id}");
                if (node && node.length > 0) {{
                    resolve(true);
                }} else {{
                    setTimeout(check, 100);
                }}
            }};
            check();
        }});
    }}""")


def select_node(_id, frame):
    frame.evaluate(f"""() => {{
        {ASSIGN_CY}
        cy.getElementById("{_id}").select();
    }}""")
    expect(frame.locator("#infopanel[data-expanded='true']")).to_be_attached(
        timeout=10000
    )


def value_for_key(frame, key):
    """The .infopanel__val of the prop row whose key is `key`."""
    return frame.locator(".infopanel__prop", has_text=key).locator(
        ".infopanel__val"
    )


def get_edge_count(frame):
    return frame.evaluate(f"""() => {{
        {ASSIGN_CY}
        return cy.edges().length;
    }}""")


def get_meta_edge_count(frame):
    return frame.evaluate(f"""() => {{
        {ASSIGN_CY}
        return cy.edges('[_isMetaEdge]').length;
    }}""")


def _open_page(page: Page):
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")
    frame = page.frame_locator(FRAME_LOCATOR).first.locator(":root")
    expect(frame.locator("#cy")).to_be_visible(timeout=10000)
    frame.click(position={"x": 0, "y": 0})
    return frame


def test_iframe_exists_infopanel_links(page: Page):
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")
    frames = page.query_selector_all(FRAME_LOCATOR)
    assert len(frames) == 1


def test_link_rendered_as_anchor(page: Page):
    """An <a href> value renders as a real, safe clickable anchor."""
    frame = _open_page(page)
    wait_for_node("alice", frame)
    select_node("alice", frame)

    link = value_for_key(frame, "publication").locator("a")
    expect(link).to_have_count(1)
    expect(link).to_have_attribute(
        "href", "https://pubmed.ncbi.nlm.nih.gov/12345"
    )
    expect(link).to_have_attribute("target", "_blank")
    expect(link).to_have_attribute("rel", "noopener noreferrer")
    expect(link).to_have_text("PMID:12345")


def test_xss_payload_not_executed(page: Page):
    """An <img onerror=...> value is inert text; no script runs."""
    frame = _open_page(page)
    wait_for_node("alice", frame)
    select_node("alice", frame)

    # The malicious value is shown, but as text - not a live element.
    unsafe_val = value_for_key(frame, "unsafe")
    expect(unsafe_val).to_contain_text("<img")
    assert frame.locator("#infopanelProps img").count() == 0
    assert frame.locator("#infopanelProps script").count() == 0
    # The onerror handler must never have fired.
    fired = frame.evaluate("() => window.__xss_fired")
    assert not fired


def test_node_update_preserves_collapse(page: Page):
    """Updating a node's data must not re-expand collapsed edges."""
    frame = _open_page(page)
    # Wait for the initial auto-collapse to settle.
    page.wait_for_timeout(500)

    initial_meta = get_meta_edge_count(frame)
    initial_edges = get_edge_count(frame)
    assert initial_meta > 0, "Expected parallel edges to be collapsed"

    wait_for_node("alice", frame)
    select_node("alice", frame)

    # Add Note updates alice's data, triggering an element update.
    btn = frame.locator(".infopanel__action-btn[data-action-name='add_note']")
    expect(btn).to_be_visible(timeout=5000)
    btn.click()

    # Wait for the update to round-trip and the new attribute to appear.
    expect(value_for_key(frame, "note")).to_contain_text(
        "updated at", timeout=10000
    )

    # Collapse state (and edge count) must be unchanged.
    assert get_meta_edge_count(frame) == initial_meta
    assert get_edge_count(frame) == initial_edges
