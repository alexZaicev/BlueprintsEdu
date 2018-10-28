from utils.gui_utils import Themes
from abc import ABC, abstractmethod
from utils import app_utils
import pygame as pg


class Blueprint(ABC):

    def __init__(self, panel, text, blueprint):
        self.__panel = panel
        self.__text_str = text
        self.__blueprint = blueprint    # Blueprint game data type
        self.focused = False
        self.pressed = False
        self.offset = (0, 0)
        self.__x = int(panel.topleft[0] * 1.05)  # TODO improve random blueprint coordinates
        self.__y = int(panel.topleft[1] * 1.05)
        self.__width = self.__panel.width * .25  # DEFAULT SIZES
        self.__height = self.__panel.height * .2
        font = pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.__height * .2))
        self.__text = font.render(self.__text_str, True, Themes.DEFAULT_THEME.get("font"))

    def get_rect(self):
        return pg.Rect((self.__x, self.__y), (self.__width, self.__height))

    def set_topleft(self, coords):
        self.__x = coords[0]
        self.__y = coords[1]

    def set_offset(self, pos):
        x = self.__x - pos[0]
        y = self.__y - pos[1]
        self.offset = (x, y)

    def set_custom_size(self, size):
        self.__width = int(self.__panel.width * size[0])
        self.__height = int(self.__panel.height * size[1])
        # UPDATE TEXT ACCORDING TO NEW SIZE
        font = pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.__height * .2))
        self.__text = font.render(self.__text_str, True, Themes.DEFAULT_THEME.get("font"))

    def change_font(self, font):
        self.__text = font.render(self.__text_str, True, Themes.DEFAULT_THEME.get("font"))

    def get_text_rect(self):
        rect_txt = self.__text.get_rect()
        rect_txt.centerx = self.get_rect().centerx
        rect_txt.top = int(self.get_rect().top + rect_txt.height * .5)
        return rect_txt

    def get_text(self):
        return self.__text

    def is_hovered(self):
        return self.get_rect().collidepoint(pg.mouse.get_pos()) == 1

    @abstractmethod
    def get_data(self):
        return {
            "name": self.__text_str
        }
