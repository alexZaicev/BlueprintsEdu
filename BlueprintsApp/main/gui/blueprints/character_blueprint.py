import pygame as pg

from blueprints.character_blueprint import CharacterBlueprint as CB
from gui.blueprints.blueprint import Blueprint
from utils.app_utils import BlueprintError
from utils.gui_utils import Themes
from utils.string_utils import StringUtils


class CharacterBlueprint(Blueprint):

    SIZE = [.25, .2]

    def __init__(self, panel):
        Blueprint.__init__(self, panel, CB())
        self.set_custom_size(CharacterBlueprint.SIZE)
        self.parent = None
        self.change_font(pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.get_rect().height * .13)))
        self.state_pressed = [False, None]
        self.state_selection = list()
        self.color_scheme_1_pressed = [False, None]
        self.color_scheme_1_selection = list()
        self.color_scheme_2_pressed = [False, None]
        self.color_scheme_2_selection = list()
        self.color_scheme_3_pressed = [False, None]
        self.color_scheme_3_selection = list()
        self.color_scheme_1_counter, self.color_scheme_2_counter, self.color_scheme_3_counter = 0, 0, 0

    def get_data(self):
        data = super().get_data()
        data[1] = StringUtils.get_string("ID_CHARACTER")
        bp = self.get_blueprint()
        data[2] = bp.pos[0]
        data[3] = bp.pos[1]
        data[4] = bp.size[0]
        data[5] = bp.size[1]
        data[6] = bp.alive
        data[7] = bp.attributes
        data[8] = bp.functions
        data[9] = bp.sprites
        # CHECK IF PARENT HAS COLORS
        if len(self.parent.colors) < 1:
            bp.color_scheme["BODY"] = None
            bp.color_scheme["TYRES"] = None
            bp.color_scheme["WINDOWS"] = None
        data[10] = bp.color_scheme.get("BODY")
        data[11] = bp.color_scheme.get("TYRES")
        data[12] = bp.color_scheme.get("WINDOWS")
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
                    self.get_blueprint().alive = key
        elif index == 10:
            self.get_blueprint().color_scheme["BODY"] = data
        elif index == 11:
            self.get_blueprint().color_scheme["TYRES"] = data
        elif index == 12:
            self.get_blueprint().color_scheme["WINDOWS"] = data
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
        self.color_scheme_1_pressed = [False, None]
        self.color_scheme_1_selection = list()
        self.color_scheme_2_pressed = [False, None]
        self.color_scheme_2_selection = list()
        self.color_scheme_3_pressed = [False, None]
        self.color_scheme_3_selection = list()

    def update_displayed_data(self, text):
        super().update_displayed_data(text)
