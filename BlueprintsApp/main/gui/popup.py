import pygame as pg
from utils.app_utils import DisplaySettings
from utils.gui_utils import Themes


class Popup(object):

    POP_STATES = {
        "INFO": "INFO",
        "ERROR": "ERROR",
        "WARNING": "WARNING",
        "HELP": "HELP"
    }

    def __init__(self, state, message):
        object.__init__(self)
        self.__state = state
        self.__message = message
        self.__coords = (int(DisplaySettings.get_size_by_key()[0] * .5), int(DisplaySettings.get_size_by_key()[1] * .5))

    def get_rect(self, text_rect):
        rect = pg.Rect((0, 0), text_rect.size)
        rect.size = (int(rect.width * 1.2), int(rect.height * 1.5))
        rect.center = self.__coords
        return rect

    def get_text(self):
        font = pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(DisplaySettings.get_size_by_key()[1] * .05))
        txt = font.render("{} -- {}".format(self.__state, self.__message),
                          True, Themes.DEFAULT_THEME.get("text_area_text"))
        rect_txt = txt.get_rect()
        rect_txt.center = self.__coords
        return txt, rect_txt

    def draw(self, display):
        txt = self.get_text()
        if self.__state == Popup.POP_STATES["ERROR"]:
            color = Themes.DEFAULT_THEME.get("notification_error_background")
        else:
            color = Themes.DEFAULT_THEME.get("notification_background")
        pg.draw.rect(display, color, self.get_rect(txt[1]), 0)
        display.blit(txt[0], txt[1])
