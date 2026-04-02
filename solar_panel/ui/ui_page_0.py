
import pyvisual as pv

def toggle_light(arduino=None, *args, **kwargs):
    """
    Toggle light via provided arduino object. Accepts extra args from UI callbacks.
    """
    if not arduino:
        return
    try:
        arduino.write(b"LIGHT_TOGGLE\n")
    except Exception:
        pass

def create_page_0_ui(window, ui, arduino=None):
    """
    Create and return UI elements for Page 0.
    :param window: The window/container for Page 0.
    :param ui: The overall UI dict (caller-managed).
    :param arduino: Optional serial/arduino object used by callbacks.
    :return: Dictionary of UI elements.
    """
    ui_page = {}
    ui_page["Button_Light"] = pv.PvButton(
        container=window,
        x=250, y=300,
        width=200, height=50,
        text="Toggle Light"
    )

    # Wire the button callback here to capture the arduino instance
    ui_page["Button_Light"].on_click = lambda *a, **k: toggle_light(arduino, *a, **k)

    ui_page["Progressbar_0"] = pv.PvProgressBar(container=window, x=554, y=58, width=140,
        height=46, min_value=20, max_value=60, value=44,
        track_color=(192, 192, 192, 100), track_border_color=(0, 0, 0, 100), fill_color=(255, 255, 0, 100), track_corner_radius=7,
        opacity=1, idle_color=(255, 255, 255, 0), track_border_thickness=0, scale=1,
        track_height=8, is_circular=True, border_thickness=0, suffix='%',
        font='assets/fonts/Poppins/Poppins.ttf', font_size=12, font_color=(0, 0, 0, 1), font_color_hover=None,
        bold=False, italic=False, underline=False, strikeout=False,
        is_visible=True, is_disabled=False, on_hover=None, on_click=None,
        on_release=None, tag=None)

    ui_page["Power_slider"] = pv.PvSlider(container=window, x=234, y=239, width=230,
        height=50, min_value=0, max_value=100, value=50,
        track_color=(200, 200, 200, 1), track_border_color=(180, 180, 180, 1), fill_color=(219, 0, 255, 1), knob_color=(219, 0, 255, 1),
        knob_border_color=(255, 255, 255, 1), track_corner_radius=2, knob_corner_radius=11, knob_width=20,
        knob_height=20, knob_size=5, show_text=False, value_text=50,
        min_text=0, max_text=100, font='assets/fonts/Poppins/Poppins.ttf', font_size=12,
        font_color=(0, 0, 0, 1), bold=False, italic=False, underline=False,
        strikethrough=False, opacity=1, track_border_thickness=0, knob_border_thickness=3,
        track_height=10, is_visible=True, is_disabled=False)

    ui_page["Battery_Percentage"] = pv.PvText(container=window, x=546, y=0, width=155,
        height=58, idle_color=(171, 84, 220, 0), text='Battery Charge Percentage', is_visible=True,
        text_alignment='left', paddings=(0, 0, 0, 0), font='assets/fonts/Montserrat/Montserrat.ttf', font_size=20,
        font_color=(122, 166, 238, 1), bold=False, italic=False, underline=False,
        strikethrough=False, opacity=1, border_color=None, corner_radius=0,
        on_hover=None, on_click=None, on_release=None, tag=None)

    ui_page["title_text"] = pv.PvText(container=window, x=217, y=210, width=264,
        height=29, idle_color=(171, 84, 220, 0), text='control the energy output ', is_visible=True,
        text_alignment='left', paddings=(0, 0, 0, 0), font='assets/fonts/Montserrat/Montserrat.ttf', font_size=20,
        font_color=(122, 166, 238, 1), bold=False, italic=False, underline=False,
        strikethrough=False, opacity=1, border_color=None, corner_radius=0,
        on_hover=None, on_click=None, on_release=None, tag=None)

    return ui_page
