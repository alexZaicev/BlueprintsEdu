import pygame as pg
from utils import app_utils


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
        self.__coords = (int(app_utils.BOARD_WIDTH * .5), int(app_utils.BOARD_HEGHT * .5))

    def get_rect(self, text_rect):
        rect = pg.Rect((0, 0), text_rect.size)
        rect.size = (int(rect.width * 1.2), int(rect.height * 1.5))
        rect.center = self.__coords
        return rect

    def get_text(self, theme):
        font = pg.font.Font(theme.get("text_font_style"), int(app_utils.BOARD_HEGHT * .05))
        txt = font.render("{} -- {}".format(self.__state, self.__message), True, theme.get("text_area_text"))
        rect_txt = txt.get_rect()
        rect_txt.center = self.__coords
        return (txt, rect_txt)

    def draw(self, display, theme):
        txt = self.get_text(theme)
        if self.__state == Popup.POP_STATES["ERROR"]:
            color = theme.get("notification_error_background")
        else:
            color = theme.get("notification_background")
        pg.draw.rect(display, color, self.get_rect(txt[1]), 0)
        display.blit(txt[0], txt[1])
