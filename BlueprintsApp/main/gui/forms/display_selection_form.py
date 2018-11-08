from gui.forms.form import Form
from utils.gui_utils import Themes
from utils.string_utils import StringUtils
from utils.app_utils import DisplaySettings, Images
import pygame as pg
from utils import app_utils
from pygame.locals import *


class DisplaySelectionForm(Form):

    def __init__(self, display, coords=None, size=None):
        Form.__init__(self, display, coords, size)
        self.size_select = None
        self.btn_drop_down = None
        self.__size = DisplaySettings.get_size_name()
        self.__size_content = list()
        self.__size_counter = 0
        self.__is_drop_down_pressed = False
        self.__selected = False

    def get_icon(self, menu):
        img = pg.image.load(Images.DROP_DOWN)
        img_rect = img.get_rect()
        img_rect.midright = (
            int(menu.right - app_utils.BOARD_WIDTH * .01), int(menu.center[1]))
        return img, img_rect

    def draw_form(self):
        super().draw_form()
        if self.visible:
            font = pg.font.Font(Themes.DEFAULT_THEME.get("banner_font_style"), int(self.size[1] * .07))
            txt = font.render(StringUtils.get_string("ID_DISPLAY"), True, Themes.DEFAULT_THEME.get("font"))
            rect_txt = txt.get_rect()
            rect_txt.topleft = (int(self.coords[0] * 1.05), int(self.coords[1] * 1.05))
            self.display.blit(txt, rect_txt)

            self.size_select = pg.Rect(
                (0, int(rect_txt.bottom * 1.2)), (int(self.size[0] * .85), int(self.size[1] * .12)))
            self.size_select.centerx = self.get_rect().centerx
            img = self.get_icon(self.size_select)
            self.btn_drop_down = img[1]
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("text_area_background"), self.size_select, 0)
            self.display.blit(img[0], img[1])

            font = pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.size_select.height * 0.6))
            txt = font.render(self.__size, True, Themes.DEFAULT_THEME.get("text_area_text"))
            rect_txt = txt.get_rect()
            rect_txt.center = self.size_select.center
            self.display.blit(txt, rect_txt)
            self.draw_drop_down()

    def draw_drop_down(self):
        if self.__is_drop_down_pressed:
            self.__size_content.clear()
            for pos in range(self.__size_counter, len(DisplaySettings.SCREEN_SIZES), 1):
                if (pos - self.__size_counter) < 3:
                    rect = pg.Rect((self.size_select.x, int(self.size_select.y +
                                                            self.size_select.height * (
                                                                        (pos - self.__size_counter) + 1))),
                                   self.size_select.size)
                    font = pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"),
                                        int(self.size_select.height * 0.6))
                    txt = font.render(DisplaySettings.get_size_name(DisplaySettings.get_size_by_id(pos)), True,
                                      Themes.DEFAULT_THEME.get("text_area_text"))
                    rect_txt = txt.get_rect()
                    rect_txt.center = rect.center
                    self.__size_content.append([rect, txt, rect_txt])

            for i in range(0, len(self.__size_content), 1):
                pg.draw.rect(self.display, Themes.DEFAULT_THEME.get(
                    "text_area_background"), self.__size_content[i][0], 0)
                self.display.blit(
                    self.__size_content[i][1], self.__size_content[i][2])

    def check_menu_pressed(self, pos):
        if self.__is_drop_down_pressed:
            for i in range(0, len(self.__size_content), 1):
                if self.__size_content[i][0].collidepoint(pos) == 1:
                    self.__size = DisplaySettings.get_size_name(DisplaySettings.get_size_by_id(i + self.__size_counter))
                    self.__is_drop_down_pressed = False
                    self.__selected = True

    def check_form_events(self, event):
        super().check_form_events(event)
        if event.type == MOUSEBUTTONUP:
            if event.button != 4 and event.button != 5:
                pos = pg.mouse.get_pos()
                self.check_menu_pressed(pos)
                if self.btn_drop_down.collidepoint(pos) == 1:
                    if self.__is_drop_down_pressed:
                        self.__is_drop_down_pressed = False
                    else:
                        self.__is_drop_down_pressed = True
                        self.__size_counter = 0
                elif self.btn_apply.get_rect().collidepoint(pos) == 1:
                    for i in range(0, len(DisplaySettings.SCREEN_SIZES), 1):
                        if self.__size == DisplaySettings.get_size_name(DisplaySettings.get_size_by_id(i)):
                            DisplaySettings.set_size_by_key(DisplaySettings.get_size_name(DisplaySettings.get_size_by_id(i)))
                            self.display = pg.display.set_mode(DisplaySettings.DEFAULT_SCREEN_SIZE)
                else:
                    self.__is_drop_down_pressed = False
        elif event.type == MOUSEBUTTONDOWN:
            if self.__is_drop_down_pressed:
                if event.button == 4:
                    self.__size_counter -= 1
                elif event.button == 5 and len(Themes.THEMES) > 3:
                    self.__size_counter += 1
                if self.__size_counter < 0:
                    self.__size_counter = 0
                elif (len(DisplaySettings.SCREEN_SIZES) > 3) and (
                        self.__size_counter > len(DisplaySettings.SCREEN_SIZES) - 3):
                    self.__size_counter = (len(DisplaySettings.SCREEN_SIZES) - 3)
