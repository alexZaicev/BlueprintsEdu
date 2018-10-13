from utils.utils import Utils

CAPTION = "BlueprintEdu V1.0"

# WINDOW SIZING
BOARD_WIDTH = 1280
BOARD_HEGHT = 800

# FRAMES PER SECOND
FPS = 90

# COLORS


class Colors(Utils):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    DIM_GREY = (105, 105, 105)
    GREY = (128, 128, 128)
    DARK_GREY = (169, 169, 169)
    SILVER = (192, 192, 192)
    LIGHT_GREY = (211, 211, 211)
    GAINSBORO = (220, 220, 220)
    WHITE_SMOKE = (245, 245, 245)
    SLATE_GREY = (112, 128, 144)
    LIGHT_SLATE_GREY = (119, 136, 153)
    DARK_ORANGE = (255, 140, 0)
    RANGE_RED = (255, 69, 0)
    DEEP_SKY_BLUE = (0, 191, 255)


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
        ["CAR_SIMULATOR_API", "Car Simulator"]
    ]

    @staticmethod
    def get_api(id):
        return GameApi.APIS[id]
