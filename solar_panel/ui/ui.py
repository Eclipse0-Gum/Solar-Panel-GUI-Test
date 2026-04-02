import pyvisual as pv
from ui.ui_page_0 import create_page_0_ui, toggle_light


def create_window():
    window = pv.PvWindow(
        title="PyVisual Window",
        width=700,
        height=400,
        bg_color=(255, 255, 255, 1),
        icon=None,
        bg_image="assets/background/background.jpg",
        is_frameless=False,
        is_resizable=False
    )
    return window


def create_pages(window):
    pages = pv.PvPages(window, animation_duration=0, animation_orientation="horizontal")
    page_0 = pages.create_page("page_0",   bg_color=(255, 255, 255, 1),  bg_image="assets/background/background.jpg")
    return pages, page_0


def create_ui(arduino=None):
    """
    Create UI and optionally forward an arduino/serial object to page UIs so callbacks can use it.
    :param arduino: optional serial/arduino object for callbacks
    :return: dict of UI elements
    """
    window = create_window()
    pages, page_0 = create_pages(window)
    page_0_widget = pages.widget(page_0)
    ui = {
        "window": window,
        "pages": pages
    }
    # forward arduino if available
    ui_page_0 = create_page_0_ui(page_0_widget, ui, arduino)

    ui.update({
        "page_0": ui_page_0
    })

    return ui


def set_arduino(ui, arduino):
    """
    Wire an existing UI to an arduino/serial object after UI creation.
    Safely no-ops if expected elements are missing.
    """
    if not ui or "page_0" not in ui:
        return
    page = ui["page_0"]
    btn = page.get("Button_Light")
    if btn is None:
        return
    btn.on_click = lambda *a, **k: toggle_light(arduino, *a, **k)
