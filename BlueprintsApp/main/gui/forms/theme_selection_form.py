from gui.forms.form import Form
import pygame as pg
from utils.gui_utils import Themes
from utils.string_utils import StringUtils
from utils.app_utils import Images
from utils import app_utils
from pygame.locals import *
from utils import logger_utils


class ThemeSelectionForm(Form):

    def __init__(self, display, coords=None, size=None):
        Form.__init__(self, display, coords, size)
        self.__logger = logger_utils.get_logger(__name__)
        self.theme_select = None
        self.btn_drop_down = None
        self.__theme = Themes.to_string(Themes.get_value(Themes.DEFAULT_THEME))
        self.__theme_content = list()
        self.__is_drop_down_pressed = False
        self.__theme_counter = 0

    def get_icon(self, menu):
        img = pg.image.load(Images.DROP_DOWN)
        img_rect = img.get_rect()
        img_rect.midright = (
            int(menu.right - app_utils.BOARD_WIDTH * .01), int(menu.center[1]))
        return (img, img_rect)

    def draw_form(self):
        super().draw_form()
        if self.visible:
            font = pg.font.Font(Themes.DEFAULT_THEME.get("banner_font_style"), int(self.size[1] * .07))
            txt = font.render(StringUtils.get_string("ID_THEME"), True, Themes.DEFAULT_THEME.get("font"))
            rect_txt = txt.get_rect()
            rect_txt.topleft = (int(self.coords[0] * 1.05), int(self.coords[1] * 1.05))
            self.display.blit(txt, rect_txt)

            self.theme_select = pg.Rect(
                (0, int(rect_txt.bottom * 1.2)), (int(self.size[0] * .85), int(self.size[1] * .12)))
            self.theme_select.centerx = self.get_rect().centerx
            img = self.get_icon(self.theme_select)
            self.btn_drop_down = img[1]
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("text_area_background"), self.theme_select, 0)
            self.display.blit(img[0], img[1])
            font = pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.theme_select.height * 0.6))

            txt = font.render(self.__theme, True, Themes.DEFAULT_THEME.get("text_area_text"))
            rect_txt = txt.get_rect()
            rect_txt.center = self.theme_select.center
            self.display.blit(txt, rect_txt)
            self.draw_drop_down()

    def draw_drop_down(self):
        if self.__is_drop_down_pressed:
            self.__theme_content.clear()
            for pos in range(self.__theme_counter, len(Themes.THEMES), 1):
                if (pos - self.__theme_counter) < 3:
                    rect = pg.Rect((self.theme_select.x, int(self.theme_select.y +
                                                             self.theme_select.height * ((pos - self.__theme_counter) + 1))),
                                   self.theme_select.size)
                    font = pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"),
                                        int(self.theme_select.height * 0.6))
                    txt = font.render(StringUtils.get_string(Themes.THEMES[pos][1]), True, Themes.DEFAULT_THEME.get("text_area_text"))
                    rect_txt = txt.get_rect()
                    rect_txt.center = rect.center
                    self.__theme_content.append([rect, txt, rect_txt])

            for i in range(0, len(self.__theme_content), 1):
                pg.draw.rect(self.display, Themes.DEFAULT_THEME.get(
                    "text_area_background"), self.__theme_content[i][0], 0)
                self.display.blit(
                    self.__theme_content[i][1], self.__theme_content[i][2])

    def check_menu_pressed(self, pos):
        if self.__is_drop_down_pressed:
            for i in range(0, len(self.__theme_content), 1):
                if self.__theme_content[i][0].collidepoint(pos) == 1:
                    self.__theme = StringUtils.get_string(Themes.THEMES[i + self.__theme_counter][1])
                    self.__is_drop_down_pressed = False
                    self.__selected = True

    def check_form_events(self, event):
        super().check_form_events(event)
        if event.type == MOUSEBUTTONUP:
            if event.button != 4 and event.button != 5:
                pos = pg.mouse.get_pos()
                if self.btn_drop_down.collidepoint(pos) == 1:
                    if self.__is_drop_down_pressed:
                        self.__is_drop_down_pressed = False
                    else:
                        self.__is_drop_down_pressed = True
                        self.__theme_counter = 0
                elif self.btn_apply.get_rect().collidepoint(pos) == 1:
                    for i in range(0, len(Themes.THEMES), 1):
                        if self.__theme == Themes.THEMES[i][1]:
                            Themes.set_theme(Themes.THEMES[i][0])
                self.check_menu_pressed(pos)
        elif event.type == MOUSEBUTTONDOWN:
            if self.__is_drop_down_pressed:
                if event.button == 4:
                    self.__theme_counter -= 1
                elif event.button == 5 and len(Themes.THEMES) > 3:
                    self.__theme_counter += 1
                if self.__theme_counter < 0:
                    self.__theme_counter = 0
                elif (len(Themes.THEMES) > 3) and (self.__theme_counter > len(Themes.THEMES) - 3):
                    self.__theme_counter = (len(Themes.THEMES) - 3)
