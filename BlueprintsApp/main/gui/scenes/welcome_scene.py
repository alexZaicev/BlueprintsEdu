from gui.scenes.scene_builder import SceneBuilder
from utils import logger_utils
from utils import app_utils
from utils.app_utils import Colors, Fonts
import pygame as pg
from gui.buttons.new_button import NewButton
from gui.buttons.load_button import LoadButton
from gui.buttons.configuration_button import ConfigurationButton
from gui.buttons.exit_button import ExitButton
from pygame.locals import *
from utils.string_utils import StringUtils

class WelcomeScene(SceneBuilder):

    def __init__(self, display, theme):
        SceneBuilder.__init__(self, display, theme)
        self.logger = logger_utils.get_logger(__name__)
        self.btn_new = NewButton(theme, 0)
        self.btn_load = LoadButton(theme, 1)
        self.btn_conf = ConfigurationButton(theme, 2)
        self.btn_exit = ExitButton(theme, 3)

    def draw_buttons(self):
        # PREPARE BUTTON RECTANGLES
        pg.draw.rect(self.display, self.btn_new.color, self.btn_new.get_rect(), 0)
        self.display.blit(self.btn_new.get_text(), self.btn_new.get_text_rect())
        pg.draw.rect(self.display, self.btn_load.color, self.btn_load.get_rect(), 0)
        self.display.blit(self.btn_load.get_text(), self.btn_load.get_text_rect())
        pg.draw.rect(self.display, self.btn_conf.color, self.btn_conf.get_rect(), 0)
        self.display.blit(self.btn_conf.get_text(), self.btn_conf.get_text_rect())
        pg.draw.rect(self.display, self.btn_exit.color, self.btn_exit.get_rect(), 0)
        self.display.blit(self.btn_exit.get_text(), self.btn_exit.get_text_rect())

    def draw_scene(self):
        # PREPARE DATA TO DISPLAY
        font = pg.font.Font(self.theme.get("banner_font_style"), int(app_utils.BOARD_HEGHT * .2))
        txt_banner = font.render(StringUtils.get_string("ID_WELCOME"), True, self.theme.get("font"))
        font = pg.font.Font(self.theme.get("banner_font_style"), int(app_utils.BOARD_HEGHT * .06))
        txt_sub_banner = font.render(app_utils.CAPTION, True, self.theme.get("font"))

        rect_banner = txt_banner.get_rect()
        rect_banner.midtop = (int(app_utils.BOARD_WIDTH / 2), int(app_utils.BOARD_HEGHT * .05))
        rect_sub_banner = txt_sub_banner.get_rect()
        rect_sub_banner.midtop = (int(app_utils.BOARD_WIDTH / 2), int(rect_banner.bottom + app_utils.BOARD_HEGHT * .02))
        # PUSH TO DISPLAY
        self.display.fill(self.theme.get("front_screen"))
        self.display.blit(txt_banner, rect_banner)
        self.display.blit(txt_sub_banner, rect_sub_banner)
        self.draw_buttons()
        self.check_button_hover()
        super().draw_scene()

    def check_events(self, event, board):
        super().check_events(event, board)
        if event.type == MOUSEBUTTONUP:
            self.check_button_press(pg.mouse.get_pos(), board)
        elif event.type == MOUSEBUTTONDOWN:
            self.check_button_press(pg.mouse.get_pos(), board, draw_boarder=True)

    def check_button_press(self, pos, board, draw_boarder=False):
        if self.btn_new.get_rect().collidepoint(pos) == 1:
            self.btn_new.on_click(board)
        elif self.btn_load.get_rect().collidepoint(pos) == 1:
            self.btn_load.on_click(board)
        elif self.btn_conf.get_rect().collidepoint(pos) == 1:
            self.btn_conf.on_click(board)
        elif self.btn_exit.get_rect().collidepoint(pos) == 1:
            self.btn_exit.on_click(board)

    def check_button_hover(self):
        # BUTTON HOVERING
        if self.btn_new.is_hovered(pg.mouse.get_pos()):
            self.btn_new.color = self.theme.get("selection_background")
        else:
            self.btn_new.color = self.theme.get("button")
        if self.btn_load.is_hovered(pg.mouse.get_pos()):
            self.btn_load.color = self.theme.get("selection_background")
        else:
            self.btn_load.color = self.theme.get("button")
        if self.btn_conf.is_hovered(pg.mouse.get_pos()):
            self.btn_conf.color = self.theme.get("selection_background")
        else:
            self.btn_conf.color = self.theme.get("button")
        if self.btn_exit.is_hovered(pg.mouse.get_pos()):
            self.btn_exit.color = self.theme.get("selection_background")
        else:
            self.btn_exit.color = self.theme.get("button")
