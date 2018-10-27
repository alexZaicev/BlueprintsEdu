from utils.utils import Utils
from utils.string_utils import StringUtils

CAPTION = "BlueprintEdu V1.0"

# WINDOW SIZING
BOARD_WIDTH = 800  # 1280
BOARD_HEGHT = 600  # 800

# FRAMES PER SECOND
FPS = 90


class DisplaySettings(Utils):

    DEFAULT_SCREEN_SIZE = [1024, 720]

    SCREEN_SIZES = {
        "800x600": [800, 600],
        "1024x720": [1024, 720]
    }

    @classmethod
    def get_size(cls, size_id):
        return DisplaySettings.SCREEN_SIZES.get(size_id)


class Colors(Utils):
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    DIM_GREY = (105, 105, 105)
    GREY = (128, 128, 128)
    DARK_GREY = (169, 169, 169)
    SILVER = (192, 192, 192)
    VAMPIRE_GREY = (64, 64, 64)
    NIGHT_GREY = (28, 28, 28)
    LIGHT_GREY = (211, 211, 211)
    GAINSBORO = (220, 220, 220)
    WHITE_SMOKE = (245, 245, 245)
    SLATE_GREY = (112, 128, 144)
    LIGHT_SLATE_GREY = (119, 136, 153)
    DARK_ORANGE = (255, 140, 0)
    RANGE_RED = (255, 69, 0)
    DEEP_SKY_BLUE = (0, 191, 255)
    LIGHT_CYAN = (224, 255, 255)
    PALE_TURQUOISE = (175, 238, 238)
    POWDER_BLUE = (176, 224, 230)
    LIGHT_BLUE = (173, 216, 230)
    LAVENDER = (230, 230, 250)
    ALICE_BLUE = (240, 248, 255)
    SNOW = (255, 250, 250)
    ORCHID = (218, 112, 214)
    HOT_PINK = (255, 105, 180)
    PALE_VIOLET_RED = (218, 112, 147)
    VIOLET = (238, 130, 238)
    PURPLE = (128, 0, 128)
    MAGENTA = (255, 0, 255)
    DEEP_PINK = (255, 20, 147)
    LIGHT_PINK = (255, 182, 193)
    PINK = (255, 192, 203)
    MEDIUM_ORCHID = (186, 85, 211)


class Fonts(Utils):
    ROOT_PATH = "resources/fonts/"
    ARCHISTICO_SIMPLE = ROOT_PATH + "Archistico_Simple.ttf"
    ARCHISTICO_BOLD = ROOT_PATH + "Archistico_Bold.ttf"
    SANSATION_BOLD = ROOT_PATH + "Sansation_Bold.ttf"
    SANSATION_BOLDITALIC = ROOT_PATH + "Sansation_BoldItalic.ttf"
    SANSATION_ITALIC = ROOT_PATH + "Sansation_Italic.ttf"
    SANSATION_LIGHT = ROOT_PATH + "Sansation_Light.ttf"
    SANSATION_LIGHTITALIC = ROOT_PATH + "Sansation_LightItalic.ttf"
    SANSATION_REGULAR = ROOT_PATH + "Sansation_Regular.ttf"


class Images(Utils):
    ROOT_PATH = "resources/images/"
    UNDO = ROOT_PATH + "undo.png"
    DROP_DOWN = ROOT_PATH + "drop-down.png"


class GameApi(Utils):
    APIS = [
        ["CAR_SIMULATOR_API", StringUtils.get_string("ID_CAR_SIMULATOR")]
    ]
    DEFAULT_API = " --- {} ---".format(StringUtils.get_string("ID_SELECT"))

    @staticmethod
    def get_api(id):
        return GameApi.APIS[id]
