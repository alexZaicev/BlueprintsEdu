from gui.scenes.scene_builder import SceneBuilder
from utils import logger_utils, app_utils
import pygame as pg
from utils.string_utils import StringUtils
from gui.buttons.config_theme_button import ConfigThemeButton
from utils.gui_utils import Themes
from gui.buttons.config_language_button import ConfigLanguageButton
from utils import gui_utils


class ConfigurationScene(SceneBuilder):

    def __init__(self, display):
        SceneBuilder.__init__(self, display)
        self.__logger = logger_utils.get_logger(__name__)
        self.btn_theme = ConfigThemeButton(0)
        self.btn_language = ConfigLanguageButton(0)

    def draw_scene(self):
        # PREPARE DATA
        font = pg.font.Font(Themes.DEFAULT_THEME.get("banner_font_style"), int(app_utils.BOARD_HEGHT * .09))
        txt = font.render(StringUtils.get_string("ID_CONFIGURATION"), True, Themes.DEFAULT_THEME.get("font"))
        rect_txt = txt.get_rect()
        rect_txt.topleft = (int(app_utils.BOARD_WIDTH * .02), int(app_utils.BOARD_HEGHT * .05))
        # DISPLAY
        self.display.fill(Themes.DEFAULT_THEME.get("front_screen"))
        self.display.blit(txt, rect_txt)
        self.draw_buttons()
        super().draw_scene()

    def draw_buttons(self):
        x = int(app_utils.BOARD_WIDTH * .02)
        y = app_utils.BOARD_HEGHT * .93
        pos = 0
        self.btn_theme.set_custom_coordinates(
            (int(x + self.btn_theme.get_rect().width * .5),
             int(y - pos * (self.btn_theme.get_rect().height + gui_utils.BUTTON_MARGIN * app_utils.BOARD_HEGHT))))
        pg.draw.rect(self.display, self.btn_theme.color, self.btn_theme.get_rect(), 0)
        self.display.blit(self.btn_theme.get_text(), self.btn_theme.get_text_rect())
        pos += 1
        self.btn_language.set_custom_coordinates(
            (int(x + self.btn_language.get_rect().width * .5),
             int(y - pos * (self.btn_language.get_rect().height + gui_utils.BUTTON_MARGIN * app_utils.BOARD_HEGHT))))
        pg.draw.rect(self.display, self.btn_language.color, self.btn_language.get_rect(), 0)
        self.display.blit(self.btn_language.get_text(), self.btn_language.get_text_rect())

    def check_events(self, event, board):
        super().check_events(event, board)
