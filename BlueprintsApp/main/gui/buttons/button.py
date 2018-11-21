from abc import ABC, abstractmethod
import pygame as pg
from utils import gui_utils
from utils.gui_utils import Themes
from utils import logger_utils
from utils.app_utils import DisplaySettings


class Button(ABC):

    def __init__(self, text, pos):
        font = pg.font.Font(Themes.DEFAULT_THEME.get("button_font_style"),
                            int(DisplaySettings.get_size_by_key()[1] * .045))
        self.logger = logger_utils.get_logger(__name__)
        self.__text_str = text
        self.__text = font.render(text, True, Themes.DEFAULT_THEME.get("font"))
        self.__height = int(font.size(self.__text_str)[1] * 1.1)
        self.__width = int(font.size(self.__text_str)[0] * 1.1)
        self.color = Themes.DEFAULT_THEME.get("button")  # Default color but overrides in scene drawings
        self.__x, self.__y = self.set_coordinates(pos)

    @abstractmethod
    def update_button(self, text, color):
        self.__text_str = text
        font = pg.font.Font(Themes.DEFAULT_THEME.get("button_font_style"),
                            int(DisplaySettings.get_size_by_key()[1] * .045))
        self.__height = int(font.size(self.__text_str)[1] * 1.1)
        self.__width = int(font.size(self.__text_str)[0] * 1.1)
        self.__text = font.render(self.__text_str, True, Themes.DEFAULT_THEME.get("font"))

    @abstractmethod
    def on_click(self, board, form=None):
        pass

    def get_text(self):
        return self.__text

    def get_color(self):
        return self.color

    def set_coordinates(self, pos):
        x = int(gui_utils.BUTTON_MARGIN * DisplaySettings.get_size_by_key()[0] + self.__width * .5)
        start = int(
            DisplaySettings.get_size_by_key()[1] - (DisplaySettings.get_size_by_key()[1] * 0.05 + self.__height * .5))
        if pos > 0:
            y = int(start - (self.__height + int(gui_utils.BUTTON_MARGIN * DisplaySettings.get_size_by_key()[1])) * pos)
        else:
            y = start
        return x, y

    def set_custom_coordinates(self, pos):
        self.__x, self.__y = pos

    def set_custom_size(self, size):
        self.__height = int(DisplaySettings.get_size_by_key()[1] * size[1])
        font = pg.font.Font(Themes.DEFAULT_THEME.get("button_font_style"), int(self.__height * .5))
        self.__text = font.render(self.__text_str, True, Themes.DEFAULT_THEME.get("font"))
        self.__width = int(font.size(self.__text_str)[0] * size[0])

    def get_topleft(self):
        x = self.__x - int(self.__width * .5)
        y = self.__y - int(self.__height * .5)
        return x, y

    def set_topleft(self, coords):
        if len(coords) == 2:
            self.__x = int(coords[0] + self.__width * .5)
            self.__y = int(coords[1] + self.__height * .5)
        else:
            self.__x = int(coords[0] + self.__width * .5)

    def is_hovered(self, coords):
        r = self.get_rect()
        return (r.x <= coords[0] <= (r.x + r.width) and
                r.y <= coords[1] <= (r.y + r.height))

    def get_rect(self):
        return pg.Rect(self.get_topleft(), (self.__width, self.__height))

    def get_text_rect(self):
        text_rect = self.__text.get_rect()
        text_rect.center = self.get_rect().center
        return text_rect

    def change_font_color(self, color):
        font = pg.font.Font(Themes.DEFAULT_THEME.get("button_font_style"), int(self.__height * .5))
        self.__text = font.render(self.__text_str, True, color)
