from utils.app_utils import Fonts
from utils.app_utils import Colors
from utils.utils import Utils
from utils import logger_utils
from utils.string_utils import StringUtils


# CONTROL PANEL
CP_WIDTH = .3
CP_HEIGHT = 1.0

# BUTTON PANEL
BP_WIDTH = 0.68
BP_HEIGHT = 0.08

# BLUEPRINT CANVAS
BC_WIDTH = .68
BC_HEIGHT = 0.9


class Themes(Utils):
    LOGGER = logger_utils.get_logger(__name__)

    # STYLING THEMES
    DARK_KNIGHT = "ST_0"
    DAY_LIGHT = "ST_1"
    PRINCESS = "ST_2"

    # THEME STYLE MAP
    DARK_KNIGHT_DICT = {
        "font": Colors.WHITE,
        "button_font_style": Fonts.NOTO_SANS_CJK_MEDIUM,
        "banner_font_style": Fonts.NOTO_SANS_CJK_MEDIUM,
        "text_font_style": Fonts.NOTO_SANS_CJK_MEDIUM,
        "font_error": Colors.RANGE_RED,
        "background": Colors.BLACK,
        "button": Colors.LIGHT_GREY,
        "button_dark": Colors.VAMPIRE_GREY,
        "panel_disabled": Colors.NIGHT_GREY,
        "panel_background": Colors.GREY,
        "panel_front_light": Colors.SILVER,
        "panel_front_dark": Colors.SLATE_GREY,
        "line_separation": Colors.BLACK,
        "notification_background": Colors.WHITE_SMOKE,
        "notification_error_background": Colors.DARK_ORANGE,
        "selection_background": Colors.DEEP_SKY_BLUE,
        "selection_boarder": Colors.BLACK,
        "selection_font": Colors.BLACK,
        "front_screen": Colors.DIM_GREY,
        "text_area_background": Colors.WHITE,
        "text_area_text": Colors.BLACK,
        "menu_background": Colors.DARK_GREY,
        "idle_blueprint": Colors.VAMPIRE_GREY,
        "active_blueprint": Colors.SILVER,
        "enabled_blueprint": Colors.SLATE_GREY,
        "connection_line": Colors.RED,
        "drop_down_item": Colors.LIGHT_GREY
    }
    DAY_LIGHT_DICT = {
        "font": Colors.BLACK,
        "button_font_style": Fonts.NOTO_SANS_CJK_MEDIUM,
        "banner_font_style": Fonts.NOTO_SANS_CJK_MEDIUM,
        "text_font_style": Fonts.NOTO_SANS_CJK_MEDIUM,
        "font_error": Colors.RANGE_RED,
        "background": Colors.WHITE,
        "button": Colors.GAINSBORO,
        "panel_background": Colors.LIGHT_GREY,
        "panel_disabled": Colors.NIGHT_GREY,
        "panel_front_light": Colors.LIGHT_CYAN,
        "panel_front_dark": Colors.LAVENDER,
        "line_separation": Colors.BLACK,
        "notification_background": Colors.WHITE_SMOKE,
        "notification_error_background": Colors.DARK_ORANGE,
        "selection_background": Colors.GREY,
        "selection_boarder": Colors.BLACK,
        "selection_font": Colors.BLACK,
        "front_screen": Colors.SNOW,
        "text_area_background": Colors.PALE_TURQUOISE,
        "text_area_text": Colors.BLACK,
        "menu_background": Colors.POWDER_BLUE,
        "idle_blueprint": Colors.VAMPIRE_GREY,
        "active_blueprint": Colors.SILVER,
        "enabled_blueprint": Colors.SLATE_GREY,
        "connection_line": Colors.RED
    }
    PRINCESS_DICT = {
        "font": Colors.WHITE,
        "button_font_style": Fonts.NOTO_SANS_CJK_MEDIUM,
        "banner_font_style": Fonts.NOTO_SANS_CJK_MEDIUM,
        "text_font_style": Fonts.NOTO_SANS_CJK_MEDIUM,
        "font_error": Colors.RANGE_RED,
        "background": Colors.PINK,
        "button": Colors.MEDIUM_ORCHID,
        "panel_background": Colors.HOT_PINK,
        "panel_disabled": Colors.NIGHT_GREY,
        "panel_front_light": Colors.PINK,
        "panel_front_dark": Colors.MEDIUM_ORCHID,
        "line_separation": Colors.PURPLE,
        "notification_background": Colors.VIOLET,
        "notification_error_background": Colors.DARK_ORANGE,
        "selection_background": Colors.MAGENTA,
        "selection_boarder": Colors.PALE_VIOLET_RED,
        "selection_font": Colors.MEDIUM_ORCHID,
        "front_screen": Colors.DEEP_PINK,
        "text_area_background": Colors.PINK,
        "text_area_text": Colors.WHITE,
        "menu_background": Colors.PURPLE,
        "idle_blueprint": Colors.VAMPIRE_GREY,
        "active_blueprint": Colors.SILVER,
        "enabled_blueprint": Colors.SLATE_GREY,
        "connection_line": Colors.RED
    }

    DEFAULT_THEME = DARK_KNIGHT_DICT

    THEMES = [
        [DARK_KNIGHT, "ID_DARK_KNIGHT"],
        [DAY_LIGHT, "ID_DAY_LIGHT"],
        [PRINCESS, "ID_PRINCESS"]
    ]

    @classmethod
    def set_theme(cls, style):
        if style == Themes.DARK_KNIGHT:
            Themes.DEFAULT_THEME = Themes.DARK_KNIGHT_DICT
        elif style == Themes.DAY_LIGHT:
            Themes.DEFAULT_THEME = Themes.DAY_LIGHT_DICT
        elif style == Themes.PRINCESS:
            Themes.DEFAULT_THEME = Themes.PRINCESS_DICT
        else:
            Themes.LOGGER.error("Failed to set unknown theme style")

    @classmethod
    def to_string(cls, style):
        s = ""
        if style == Themes.DARK_KNIGHT:
            s = StringUtils.get_string("ID_DARK_KNIGHT")
        elif style == Themes.DAY_LIGHT:
            s = StringUtils.get_string("ID_DAY_LIGHT")
        elif style == Themes.PRINCESS:
            s = StringUtils.get_string("ID_PRINCESS")
        return s

    @classmethod
    def get_value(cls, theme_dic):
        if theme_dic == Themes.DARK_KNIGHT_DICT:
            return Themes.DARK_KNIGHT
        elif theme_dic == Themes.DAY_LIGHT_DICT:
            return Themes.DAY_LIGHT
        elif theme_dic == Themes.PRINCESS_DICT:
            return Themes.PRINCESS


# WIDGETS
BUTTON_MARGIN = .005
BUTTON_MENU_MARGIN = 0.005
BUTTON_PRIMARY = (.24, .06)
BUTTON_MENU = ()
