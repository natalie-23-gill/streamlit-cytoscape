from playwright.sync_api import Page, expect


FRAME_LOCATOR = "iframe[title*='st_cytoscape']"


def test_run(page: Page):
    expect(page).to_have_title("Node Styles")


def test_iframe_exists(page: Page):
    # Node Styles is the default page, so iframe should already exist
    page.wait_for_load_state("networkidle")
    page.wait_for_selector(FRAME_LOCATOR, timeout=10000)
    frames = page.query_selector_all(FRAME_LOCATOR)
    assert len(frames) == 1
