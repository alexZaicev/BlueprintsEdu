from utils.app_utils import Colors
from utils.app_utils import Fonts
from utils.utils import Utils
from utils import logger_utils


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
        "button_font_style": Fonts.SANSATION_BOLD,
        "banner_font_style": Fonts.ARCHISTICO_BOLD,
        "text_font_style": Fonts.SANSATION_REGULAR,
        "font_error": Colors.DARK_ORANGE,
        "background": Colors.BLACK,
        "button": Colors.LIGHT_GREY,
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
        "text_area_text": Colors.BLACK
    }
    DAY_LIGHT_DICT = {

    }
    PRINCESS_DICT = {

    }

    DEFAULT_THEME = DARK_KNIGHT_DICT

    @classmethod
    def set_theme(cls, style):
        if style == Themes.DARK_KNIGHT:
            Themes.DEFAULT_THEME = Themes.DARK_KNIGHT_DICT
        elif style == Theme.DAY_LIGHT:
            Themes.DEFAULT_THEME = Themes.DAY_LIGHT_DICT
        elif style == Themes.PRINCESS:
            Themes.DEFAULT_THEME = Themes.PRINCESS_DICT
        else:
            Themes.LOGGER.error("Failed to set unknown theme style")


# WIDGETS
BUTTON_MARGIN = .02
BUTTON_PRIMARY = (.32, .08)
BUTTON_MENU = ()
