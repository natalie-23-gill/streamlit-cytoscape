import json
import pytest
from playwright.sync_api import Page, expect

from streamlit_cytoscape.infopanel import InfopanelAction


PAGE_NAME = "Infopanel"
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


def get_return_json(page: Page):
    data = (
        page.get_by_test_id("stJson")
        .text_content()
        .replace('""', '","')
        .replace('}"', '},"')
    )
    return json.loads(data)


# ---- Python unit tests (no Playwright) ----


def test_reserved_name_raises():
    with pytest.raises(ValueError):
        InfopanelAction("remove", "Remove")


def test_reserved_name_expand_raises():
    with pytest.raises(ValueError):
        InfopanelAction("expand", "Expand")


def test_infopanel_action_dump():
    action = InfopanelAction("my_action", "My Action", icon="search")
    dumped = action.dump()
    assert dumped == {
        "name": "my_action",
        "label": "My Action",
        "icon": "search",
    }


def test_infopanel_action_dump_no_icon():
    action = InfopanelAction("my_action", "My Action")
    dumped = action.dump()
    assert dumped == {"name": "my_action", "label": "My Action"}
    assert "icon" not in dumped


# ---- Playwright integration tests ----


def test_iframe_exists_infopanel_actions(page: Page):
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")
    frames = page.query_selector_all(FRAME_LOCATOR)
    assert len(frames) == 1


def test_action_buttons_hidden_when_deselected(page: Page):
    """Action buttons should not be visible before selection."""
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")

    frame = page.frame_locator(FRAME_LOCATOR).first.locator(":root")
    expect(frame.locator("#cy")).to_be_visible(timeout=10000)

    # Panel should be collapsed, actions not visible
    actions_container = frame.locator("#infopanelActions")
    expect(actions_container).not_to_be_visible()


def test_action_buttons_appear_when_selected(page: Page):
    """Selecting a node should show action buttons in the infopanel."""
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")

    frame = page.frame_locator(FRAME_LOCATOR).first.locator(":root")
    expect(frame.locator("#cy")).to_be_visible(timeout=10000)
    frame.click(position={"x": 0, "y": 0})

    wait_for_node("n1", frame)

    # Select node
    frame.evaluate(
        f"""() => {{
        {ASSIGN_CY}
        cy.getElementById("n1").select();
    }}"""
    )

    AWAIT_SELECT(frame)

    # Verify buttons are visible
    buttons = frame.locator(".infopanel__action-btn")
    expect(buttons.first).to_be_visible(timeout=5000)
    assert buttons.count() == 3


def test_action_button_label_displayed(page: Page):
    """Action button labels should match configured labels."""
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")

    frame = page.frame_locator(FRAME_LOCATOR).first.locator(":root")
    expect(frame.locator("#cy")).to_be_visible(timeout=10000)
    frame.click(position={"x": 0, "y": 0})

    wait_for_node("n1", frame)

    frame.evaluate(
        f"""() => {{
        {ASSIGN_CY}
        cy.getElementById("n1").select();
    }}"""
    )

    AWAIT_SELECT(frame)

    buttons = frame.locator(".infopanel__action-btn")
    expect(buttons.first).to_be_visible(timeout=5000)

    labels = [btn.text_content() for btn in buttons.all()]
    assert "AI Summary" in labels
    assert "Fetch Details" in labels
    assert "Flag for Review" in labels


def test_action_button_click_returns_data(page: Page):
    """Clicking action button should return data."""
    page.get_by_role("link", name=PAGE_NAME).click()
    page.wait_for_load_state("networkidle")

    frame = page.frame_locator(FRAME_LOCATOR).first.locator(":root")
    expect(frame.locator("#cy")).to_be_visible(timeout=10000)
    frame.click(position={"x": 0, "y": 0})

    wait_for_node("n1", frame)

    frame.evaluate(
        f"""() => {{
        {ASSIGN_CY}
        cy.getElementById("n1").select();
    }}"""
    )

    AWAIT_SELECT(frame)

    # Click the "AI Summary" button
    selector = ".infopanel__action-btn[data-action-name='ai_summary']"
    ai_btn = frame.locator(selector)
    expect(ai_btn).to_be_visible(timeout=5000)
    ai_btn.click()

    # Wait for return value to appear
    page.get_by_text('"action":"').click(timeout=10000)
    data = get_return_json(page)

    assert data["action"] == "ai_summary"
    assert data["data"]["element_id"] == "n1"
    assert data["data"]["element_group"] == "nodes"
    assert "element_data" in data["data"]
