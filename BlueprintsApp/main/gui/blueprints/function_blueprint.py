from gui.blueprints.blueprint import Blueprint
from utils.string_utils import StringUtils
import pygame as pg
from utils.gui_utils import Themes
from blueprints.function_blueprint import FunctionBlueprint as FB


class FunctionBlueprint(Blueprint):

    SIZE = [.25, .2]

    def __init__(self, panel):
        Blueprint.__init__(self, panel, FB())
        self.set_custom_size(FunctionBlueprint.SIZE)
        self.change_font(pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.get_rect().height * .13)))

    def get_data(self):
        data = super().get_data()
        data[1] = StringUtils.get_string("ID_FUNCTION")
        return data

    def set_data(self, index, data):
        super().set_data(index, data)
        self.update_displayed_data(self.font.render("{}()".format(self.get_blueprint().name),
                                                    True, Themes.DEFAULT_THEME.get("font")))

    def initialize(self, coords, size, blueprint, panel):
        super().initialize(coords, size, blueprint, panel)
        self.change_font(pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.get_rect().height * .13)))
        self.update_displayed_data(self.font.render("{}()".format(self.get_blueprint().name),
                                                    True, Themes.DEFAULT_THEME.get("font")))
        # TODO add additional data

    def reset_selection(self):
        super().reset_selection()

    def update_displayed_data(self, text):
        super().update_displayed_data(text)
