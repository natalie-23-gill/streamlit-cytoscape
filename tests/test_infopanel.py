from playwright.sync_api import Page, expect


PAGE_NAME = "Infopanel"
FRAME_LOCATOR = "iframe[title*='streamlit_cytoscape']"
ASSIGN_CY = "const cy = document.getElementById('cy')._cyreg.cy;"


def get_node_pos(_id, iframe):
    pos = iframe.evaluate(
        f"""() => {{
        {ASSIGN_CY}
        return cy.getElementById("{_id}").renderedPosition();
    }}"""
    )
    return pos


def AWAIT_SELECT(frame):
    infopanel = frame.locator("#infopanel[data-expanded='true']")
    expect(infopanel).to_be_attached(timeout=10000)


def get_infopanel_props(frame):
    """Get all property keys displayed in the infopanel."""
    props = frame.locator(".infopanel__key")
    return [prop.text_content() for prop in props.all()]


def test_iframe_exists_infopanel(page: Page):
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")
    frames = page.query_selector_all(FRAME_LOCATOR)
    assert len(frames) == 1


def wait_for_node(_id, frame):
    """Wait for a node to exist in Cytoscape graph."""
    frame.evaluate(
        f"""() => {{
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
    }}"""
    )


def test_hide_underscore_attrs_enabled(page: Page):
    """When hide_underscore_attrs=True, underscore-prefixed keys are hidden."""
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")

    # Wait for iframe to load
    frame = page.frame_locator(FRAME_LOCATOR).first.locator(":root")
    expect(frame.locator("#cy")).to_be_visible(timeout=10000)
    frame.click(position={"x": 0, "y": 0})  # scroll into view

    # Wait for node to be ready in Cytoscape
    wait_for_node("node1", frame)

    # Click on the node to select it using JavaScript
    frame.evaluate(
        f"""() => {{
        {ASSIGN_CY}
        cy.getElementById("node1").select();
    }}"""
    )

    # Wait for infopanel to expand
    AWAIT_SELECT(frame)

    # Get displayed properties
    props = get_infopanel_props(frame)

    # Should show regular attributes but not underscore-prefixed ones
    assert "name" in props
    assert "visible_attr" in props
    assert "_hidden_attr" not in props
    assert "_style_data" not in props


def test_hide_underscore_attrs_disabled(page: Page):
    """When hide_underscore_attrs=False, underscore-prefixed keys are shown."""
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")

    # Uncheck the "Hide underscore attributes" checkbox by clicking its text
    page.get_by_text("Hide underscore attributes").click()
    page.wait_for_load_state("networkidle")

    frame = page.frame_locator(FRAME_LOCATOR).first.locator(":root")
    frame.click(position={"x": 0, "y": 0})  # scroll into view

    # Click on the node to select it
    pos = get_node_pos("node1", frame)
    frame.click(position=pos)

    # Wait for infopanel to expand
    infopanel_label = frame.locator("#infopanelLabel")
    expect(infopanel_label).to_be_visible(timeout=10000)

    # Get displayed properties
    props = get_infopanel_props(frame)

    # Should show all attributes including underscore-prefixed ones
    assert "name" in props
    assert "visible_attr" in props
    assert "_hidden_attr" in props
    assert "_style_data" in props
