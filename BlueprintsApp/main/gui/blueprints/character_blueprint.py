from gui.blueprints.blueprint import Blueprint
from utils.app_utils import BlueprintError
from utils.string_utils import StringUtils
import pygame as pg
from utils.gui_utils import Themes
from blueprints.character_blueprint import CharacterBlueprint as CB


class CharacterBlueprint(Blueprint):

    SIZE = [.25, .2]

    def __init__(self, panel):
        Blueprint.__init__(self, panel, CB())
        self.set_custom_size(CharacterBlueprint.SIZE)
        self.parent = None
        self.change_font(pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.get_rect().height * .13)))
        self.state_pressed = [False, None]
        self.state_selection = list()

    def get_data(self):
        data = super().get_data()
        data[1] = StringUtils.get_string("ID_CHARACTER")
        data[2] = self.get_blueprint().pos[0]
        data[3] = self.get_blueprint().pos[1]
        data[4] = self.get_blueprint().size[0]
        data[5] = self.get_blueprint().size[1]
        data[6] = self.get_blueprint().alive
        data[7] = self.get_blueprint().attributes
        data[8] = self.get_blueprint().functions
        data[9] = self.get_blueprint().sprites
        return data

    def set_data(self, index, data):
        if 1 < index < 6:
            if len(data) < 1:
                data = "0"

        if index == 2:
            if 0 <= int(data) <= self.parent.size[0]:
                t = list(self.get_blueprint().pos)
                t[0] = int(data)
                self.get_blueprint().pos = t
            else:
                raise BlueprintError("Character position cannot exceed system resolution")
        elif index == 3:
            if 0 <= int(data) <= self.parent.size[1]:
                t = list(self.get_blueprint().pos)
                t[1] = int(data)
                self.get_blueprint().pos = t
            else:
                raise BlueprintError("Character position cannot exceed system resolution")
        elif index == 4:
            if 0 <= int(data) <= self.parent.size[0]:
                t = list(self.get_blueprint().size)
                t[0] = int(data)
                self.get_blueprint().size = t
            else:
                raise BlueprintError("Character size cannot exceed system resolution")
        elif index == 5:
            if 0 <= int(data) <= self.parent.size[1]:
                t = list(self.get_blueprint().size)
                t[1] = int(data)
                self.get_blueprint().size = t
            else:
                raise BlueprintError("Character size cannot exceed system resolution")
        elif index == 6:
            for key, value in Blueprint.CONDITIONAL_DICT.items():
                if data == StringUtils.get_string(value):
                    self.get_blueprint().directional = key
        super().set_data(index, data)
        self.update_displayed_data(self.font.render(self.get_blueprint().name,
                                                    True, Themes.DEFAULT_THEME.get("font")))

    def initialize(self, coords, size, blueprint, panel):
        super().initialize(coords, size, blueprint, panel)
        self.change_font(pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.get_rect().height * .13)))

    def reset_selection(self):
        super().reset_selection()
        self.state_pressed = [False, None]
        self.state_selection = list()

    def update_displayed_data(self, text):
        super().update_displayed_data(text)
