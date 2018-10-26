from abc import ABC, abstractmethod
import pygame as pg
from utils import gui_utils
from utils import app_utils
import os
from utils.gui_utils import Themes


class Button(ABC):

    def __init__(self, text, pos):
        # TODO set button size according to the text object size
        font = pg.font.Font(Themes.DEFAULT_THEME.get("button_font_style"), int(app_utils.BOARD_HEGHT * .045))
        self.__text_str = text
        self.__text = font.render(text, True, Themes.DEFAULT_THEME.get("font"))
        self.__height = int(font.size(self.__text_str)[1] * 1.1)
        self.__width = int(font.size(self.__text_str)[0] * 1.1)
        self.color = Themes.DEFAULT_THEME.get("button") # Default color but overrides in scene drawings
        self.set_coordinates(pos)

    @abstractmethod
    def update_button(self, text, color):
        self.__text_str = text
        if not self.is_hovered(pg.mouse.get_pos()):
            self.color = color
            font = pg.font.Font(Themes.DEFAULT_THEME.get("button_font_style"), int(app_utils.BOARD_HEGHT * .05))
            self.__text = font.render(self.__text_str, True, Themes.DEFAULT_THEME.get("font"))

    @abstractmethod
    def on_click(self, board):
        pass

    def get_text(self):
        return self.__text

    def get_color(self):
        return self.color

    def set_coordinates(self, pos):
        self.__x = int(gui_utils.BUTTON_MARGIN * app_utils.BOARD_WIDTH + self.__width * .5)
        # start = int(app_utils.BOARD_HEGHT * .8)
        # if pos > 0:
        #     self.__y = int(start + (self.__height + int(gui_utils.BUTTON_MARGIN * app_utils.BOARD_HEGHT)) * pos)
        # else:
        #     self.__y = start
        start = int(app_utils.BOARD_HEGHT - (app_utils.BOARD_HEGHT * 0.05 + self.__height * .5))
        if pos > 0:
            self.__y = int(start - (self.__height + int(gui_utils.BUTTON_MARGIN * app_utils.BOARD_HEGHT)) * pos)
        else:
            self.__y = start

    def set_custom_coordinates(self, pos):
        self.__x, self.__y = pos

    def set_custom_size(self, size):
        self.__height = int(app_utils.BOARD_HEGHT * size[1])
        font = pg.font.Font(Themes.DEFAULT_THEME.get("button_font_style"), int(self.__height * .5))
        self.__text = font.render(self.__text_str, True, Themes.DEFAULT_THEME.get("font"))
        self.__width = int(font.size(self.__text_str)[0] * size[0])

    def get_topleft(self):
        x = self.__x - int(self.__width * .5)
        y = self.__y - int(self.__height * .5)
        return (x, y)

    def is_hovered(self, coords):
        r = self.get_rect()
        return (coords[0] >= r.x and coords[0] <= (r.x + r.width) and
                coords[1] >= r.y and coords[1] <= (r.y + r.height))

    def get_rect(self):
        return pg.Rect(self.get_topleft(), (self.__width, self.__height))

    def get_text_rect(self):
        text_rect = self.__text.get_rect()
        text_rect.center = self.get_rect().center
        return text_rect
