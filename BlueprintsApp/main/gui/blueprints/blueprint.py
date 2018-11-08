from utils.gui_utils import Themes
from abc import ABC, abstractmethod
import pygame as pg
from random import randint


class Blueprint(ABC):

    def __init__(self, panel, blueprint):
        self.__panel = panel
        self.__blueprint = blueprint    # Blueprint game data type
        self.focused = False
        self.pressed = False
        self.offset = (0, 0)
        self.__width = self.__panel.width * .25  # DEFAULT SIZES
        self.__height = self.__panel.height * .2
        self.__x = randint(int(panel.topleft[0] * 1.05), int(panel.topleft[0] + panel.width * .9 - self.__width))
        self.__y = randint(int(panel.topleft[1] * 1.05), int(panel.topleft[1] + panel.height * .9 - self.__height))
        self.font = pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.__height * .2))
        self.__text = self.font.render(self.__blueprint.name, True, Themes.DEFAULT_THEME.get("font"))

    @abstractmethod
    def initialize(self, coords, size, blueprint, panel):
        """Description: function sets all required object attributes

        :param coords List of to integer values x and y coordinates
        :param size List of to integer value width and height
        :param blueprint Blueprint data type
        :param panel Development panel rect object
        """
        self.__panel = panel
        self.__blueprint = blueprint
        self.__x, self.__y = coords
        self.__width, self.__height = size
        self.font = pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.__height * .2))
        self.__text = self.font.render(self.__blueprint.name, True, Themes.DEFAULT_THEME.get("font"))

    def get_rect(self):
        return pg.Rect((self.__x, self.__y), (self.__width, self.__height))

    @abstractmethod
    def reset_selection(self):
        pass

    def get_blueprint(self):
        return self.__blueprint

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
        self.font = pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.__height * .2))
        self.__text = self.font.render(self.__blueprint.name, True, Themes.DEFAULT_THEME.get("font"))

    def change_font(self, font):
        self.font = font
        self.__text = self.font.render(self.__blueprint.name, True, Themes.DEFAULT_THEME.get("font"))

    @abstractmethod
    def update_displayed_data(self, text):
        self.__text = text

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
            0: self.__blueprint.name
        }

    @abstractmethod
    def set_data(self, index, data):
        if index == 0:
            self.__blueprint.name = data
