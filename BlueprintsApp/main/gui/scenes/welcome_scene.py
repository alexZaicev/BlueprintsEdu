from gui.scenes.scene_builder import SceneBuilder
from utils import logger_utils
from utils import app_utils
import pygame as pg
from gui.buttons.new_button import NewButton
from gui.buttons.load_button import LoadButton
from gui.buttons.configuration_button import ConfigurationButton
from pygame.locals import *
from utils.string_utils import StringUtils
from utils.gui_utils import Themes
from utils.app_utils import DisplaySettings


class WelcomeScene(SceneBuilder):

    def __init__(self, display):
        SceneBuilder.__init__(self, display)
        self.logger = logger_utils.get_logger(__name__)
        self.btn_new = NewButton(2)
        self.btn_new.color = Themes.DEFAULT_THEME.get("front_screen")
        self.btn_load = LoadButton(1)
        self.btn_load.color = Themes.DEFAULT_THEME.get("front_screen")
        self.btn_conf = ConfigurationButton(0)
        self.btn_conf.color = Themes.DEFAULT_THEME.get("front_screen")

    def draw_buttons(self):
        # PREPARE BUTTON RECTANGLES
        pg.draw.rect(self.display, self.btn_new.color, self.btn_new.get_rect(), 0)
        self.display.blit(self.btn_new.get_text(), self.btn_new.get_text_rect())
        pg.draw.rect(self.display, self.btn_load.color, self.btn_load.get_rect(), 0)
        self.display.blit(self.btn_load.get_text(), self.btn_load.get_text_rect())
        pg.draw.rect(self.display, self.btn_conf.color, self.btn_conf.get_rect(), 0)
        self.display.blit(self.btn_conf.get_text(), self.btn_conf.get_text_rect())

    def draw_scene(self):
        # PREPARE DATA TO DISPLAY
        font = pg.font.Font(Themes.DEFAULT_THEME.get("banner_font_style"),
                            int(DisplaySettings.get_size_by_key()[1] * .2))
        txt_banner = font.render(StringUtils.get_string("ID_WELCOME"), True, Themes.DEFAULT_THEME.get("font"))
        font = pg.font.Font(Themes.DEFAULT_THEME.get("banner_font_style"),
                            int(DisplaySettings.get_size_by_key()[1] * .06))
        txt_sub_banner = font.render(app_utils.CAPTION, True, Themes.DEFAULT_THEME.get("font"))

        rect_banner = txt_banner.get_rect()
        rect_banner.midtop = (
            int(DisplaySettings.get_size_by_key()[0] / 2), int(DisplaySettings.get_size_by_key()[1] * .05))
        rect_sub_banner = txt_sub_banner.get_rect()
        rect_sub_banner.midtop = (int(DisplaySettings.get_size_by_key()[0] / 2),
                                  int(rect_banner.bottom + DisplaySettings.get_size_by_key()[1] * .02))
        # PUSH TO DISPLAY
        self.display.fill(Themes.DEFAULT_THEME.get("front_screen"))
        self.display.blit(txt_banner, rect_banner)
        self.display.blit(txt_sub_banner, rect_sub_banner)
        self.draw_buttons()
        self.check_button_hover()
        super().draw_scene()

    def check_events(self, event, board):
        super().check_events(event, board)
        if event.type == MOUSEBUTTONDOWN:
            self.check_button_press(pg.mouse.get_pos(), board)

    def check_button_press(self, pos, board):
        if self.btn_new.get_rect().collidepoint(pos) == 1:
            self.btn_new.on_click(board)
        elif self.btn_load.get_rect().collidepoint(pos) == 1:
            self.btn_load.on_click(board)
        elif self.btn_conf.get_rect().collidepoint(pos) == 1:
            self.btn_conf.on_click(board)

    def check_button_hover(self):
        # BUTTON HOVERING
        if self.btn_new.is_hovered(pg.mouse.get_pos()):
            self.btn_new.color = Themes.DEFAULT_THEME.get("selection_background")
        else:
            self.btn_new.color = Themes.DEFAULT_THEME.get("front_screen")
        if self.btn_load.is_hovered(pg.mouse.get_pos()):
            self.btn_load.color = Themes.DEFAULT_THEME.get("selection_background")
        else:
            self.btn_load.color = Themes.DEFAULT_THEME.get("front_screen")
        if self.btn_conf.is_hovered(pg.mouse.get_pos()):
            self.btn_conf.color = Themes.DEFAULT_THEME.get("selection_background")
        else:
            self.btn_conf.color = Themes.DEFAULT_THEME.get("front_screen")
