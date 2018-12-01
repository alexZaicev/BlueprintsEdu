import pygame as pg

from blueprints.sprite_blueprint import SpriteBlueprint as SB
from gui.blueprints.blueprint import Blueprint
from utils.gui_utils import Themes
from utils.string_utils import StringUtils


class SpriteBlueprint(Blueprint):

    SIZE = [.25, .2]

    def __init__(self, panel):
        Blueprint.__init__(self, panel, SB())
        self.set_custom_size(SpriteBlueprint.SIZE)
        self.change_font(pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.get_rect().height * .13)))

    def get_data(self):
        data = super().get_data()
        data[1] = StringUtils.get_string("ID_SPRITE")
        return data

    def set_data(self, index, data):
        super().set_data(index, data)
        self.update_displayed_data(self.font.render(self.get_blueprint().name,
                                                    True, Themes.DEFAULT_THEME.get("font")))

    def initialize(self, coords, size, blueprint, panel):
        super().initialize(coords, size, blueprint, panel)
        self.change_font(pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.get_rect().height * .13)))

    def reset_selection(self):
        super().reset_selection()

    def update_displayed_data(self, text):
        super().update_displayed_data(text)
