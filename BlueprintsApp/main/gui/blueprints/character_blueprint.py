from gui.blueprints.blueprint import Blueprint
from utils.string_utils import StringUtils
import pygame as pg
from utils.gui_utils import Themes
from blueprints.character_blueprint import CharacterBlueprint as CB


class CharacterBlueprint(Blueprint):

    SIZE = [.25, .2]

    def __init__(self, panel):
        Blueprint.__init__(self, panel, CB())
        self.set_custom_size(CharacterBlueprint.SIZE)
        self.change_font(pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.get_rect().height * .13)))

    def get_data(self):
        data = super().get_data()
        data[1] = StringUtils.get_string("ID_CHARACTER")
        data[2] = self.get_blueprint().attributes
        data[3] = self.get_blueprint().functions
        data[4] = self.get_blueprint().sprites
        return data

    def set_data(self, index, data):
        super().set_data(index, data)

    def initialize(self, coords, size, blueprint, panel):
        super().initialize(coords, size, blueprint, panel)
        self.change_font(pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.get_rect().height * .13)))

    def reset_selection(self):
        super().reset_selection()
