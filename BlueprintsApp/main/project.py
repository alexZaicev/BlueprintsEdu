import pygame as pg
from utils.gui_utils import Themes


class Project(object):

    def __init__(self, directory, date):
        object.__init__(self)
        self.__dir = directory
        self.__date = date
        self.pressed = False
        self.__rect = None

    def set_rect(self, container, pos):
        section_height = int(container.height / 10)
        self.__rect = pg.Rect((container.x, (container.y + section_height*pos)), (container.width, section_height))

    def get_rect(self):
        return self.__rect

    def get_name(self):
        return self.__dir

    def get_texts(self, container, pos):
        section_height = int(container.height / 10)
        font = pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(section_height * .70))
        fn = font.render(self.__dir, True, Themes.DEFAULT_THEME.get("font"))
        fn_rect = fn.get_rect()
        fn_rect.topleft = (int(container.x + (container.width * .015)),
                           int(container.midtop[1] * .98 + section_height*pos))
        dt = font.render(self.__date, True, Themes.DEFAULT_THEME.get("font"))
        dt_rect = dt.get_rect()
        dt_rect.topleft = (int((container.x + container.width) - (container.width * .015 + dt_rect.width)),
                           int(container.midtop[1] * .98 + section_height*pos))
        return (fn, fn_rect), (dt, dt_rect)
