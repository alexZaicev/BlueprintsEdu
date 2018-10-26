from utils.gui_utils import Themes
from utils import app_utils
import pygame as pg


class Blueprint(object):

    def __init__(self, panel, text, blueprint):
        self.__panel = panel
        self.__text_str = text
        self.__blueprint = blueprint    # Blueprint game data type
        self.__x = panel.topleft[0]  # TODO improve random blueprint coordinates
        self.__y = panel.topleft[1]
        self.__width = self.__panel.width * .25
        self.__height = self.__panel.height * .2
        font = pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.__height * .2))
        self.__text = font.render(self.__text_str, True, Themes.DEFAULT_THEME.get("font"))

    def get_rect(self):
        return pg.Rect((self.__x, self.__y), (self.__width, self.__height))

    def get_text_rect(self):
        rect_txt = self.__text.get_rect()
        rect_txt.centerx = self.get_rect().centerx
        rect_txt.top = self.get_rect().top * 1.1
        return rect_txt
