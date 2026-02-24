from playwright.sync_api import Page, expect


PAGE_NAME = "Infopanel Actions"
FRAME_LOCATOR = "iframe[title*='streamlit_cytoscape']"
ASSIGN_CY = "const cy = document.getElementById('cy')._cyreg.cy;"


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


def AWAIT_SELECT(frame):
    infopanel = frame.locator("#infopanel[data-expanded='true']")
    expect(infopanel).to_be_attached(timeout=10000)


def select_node(frame):
    """Select node n1 to expand the infopanel."""
    wait_for_node("n1", frame)
    frame.evaluate(
        f"""() => {{
        {ASSIGN_CY}
        cy.getElementById("n1").select();
    }}"""
    )
    AWAIT_SELECT(frame)


def test_resize_handle_visible_when_expanded(page: Page):
    """Resize handle hidden when collapsed, visible when expanded."""
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")

    frame = page.frame_locator(FRAME_LOCATOR).first.locator(":root")
    expect(frame.locator("#cy")).to_be_visible(timeout=10000)
    frame.click(position={"x": 0, "y": 0})

    resize_handle = frame.locator("#infopanelResize")

    # Before selection: handle should not be visible
    expect(resize_handle).not_to_be_visible()

    # Select node to expand panel
    select_node(frame)

    # After selection: handle should be visible
    expect(resize_handle).to_be_visible(timeout=5000)


def test_resize_changes_panel_width(page: Page):
    """Dragging resize handle should change panel width."""
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")

    frame = page.frame_locator(FRAME_LOCATOR).first.locator(":root")
    expect(frame.locator("#cy")).to_be_visible(timeout=10000)
    frame.click(position={"x": 0, "y": 0})

    select_node(frame)

    # Get initial panel width
    initial_width = frame.evaluate(
        """() => {
        const el = document.getElementById('infopanel');
        return el.getBoundingClientRect().width;
    }"""
    )

    # Get resize handle position
    handle = frame.locator("#infopanelResize")
    handle_box = handle.bounding_box()
    assert handle_box is not None

    # Drag handle to the right by 100px
    frame.locator("#infopanelResize").hover()
    page.mouse.down()
    mid_y = handle_box["y"] + handle_box["height"] / 2
    page.mouse.move(handle_box["x"] + 100, mid_y)
    page.mouse.up()

    # Verify width increased
    new_width = frame.evaluate(
        """() => {
        const el = document.getElementById('infopanel');
        return el.getBoundingClientRect().width;
    }"""
    )
    assert new_width > initial_width


def test_resize_nodeactions_follows(page: Page):
    """nodeActions left should track panel width after resize."""
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")

    frame = page.frame_locator(FRAME_LOCATOR).first.locator(":root")
    expect(frame.locator("#cy")).to_be_visible(timeout=10000)
    frame.click(position={"x": 0, "y": 0})

    select_node(frame)

    # Get initial nodeActions inline style.left
    initial_left = frame.evaluate(
        """() => {
        const el = document.getElementById('nodeActions');
        return parseFloat(el.style.left) || 0;
    }"""
    )

    # Drag resize handle right
    handle = frame.locator("#infopanelResize")
    handle_box = handle.bounding_box()
    assert handle_box is not None

    frame.locator("#infopanelResize").hover()
    page.mouse.down()
    mid_y = handle_box["y"] + handle_box["height"] / 2
    page.mouse.move(handle_box["x"] + 100, mid_y)
    page.mouse.up()

    # Verify nodeActions style.left increased
    new_left = frame.evaluate(
        """() => {
        const el = document.getElementById('nodeActions');
        return parseFloat(el.style.left) || 0;
    }"""
    )
    assert new_left > initial_left
