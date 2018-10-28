from gui.blueprints.blueprint import Blueprint
from utils.string_utils import StringUtils
import pygame as pg
from utils.gui_utils import Themes


class FunctionBlueprint(Blueprint):

    SIZE = [.25, .2]

    def __init__(self, panel, blueprint):
        Blueprint.__init__(self, panel, "{}_1".format(StringUtils.get_string("ID_FUNCTION")), blueprint)
        # TODO improve random blueprint name generation
        self.set_custom_size(FunctionBlueprint.SIZE)
        self.change_font(pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.get_rect().height * .1)))

    def get_data(self):
        data = super().get_data()
        data["type"] = StringUtils.get_string("ID_FUNCTION")
        return data
