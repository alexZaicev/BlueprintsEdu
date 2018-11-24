from gui.blueprints.blueprint import Blueprint
from utils.string_utils import StringUtils
import pygame as pg
from utils.gui_utils import Themes
from blueprints.function_blueprint import FunctionBlueprint as FB


class FunctionBlueprint(Blueprint):

    SIZE = [.25, .2]
    TYPE = {
        "FUNC_M": "ID_MOVEMENT",
        "FUNC_C": "ID_CUSTOM"
    }

    """Movement functions specific data types for user to configure game object
    """
    ORIENTATION = {
        "ORIENT_UP": "ID_UP",
        "ORIENT_DOWN": "ID_DOWN",
        "ORIENT_LEFT": "ID_LEFT",
        "ORIENT_RIGHT": "ID_RIGHT"
    }

    DIRECTIONAL = {
        False: "ID_FALSE",
        True: "ID_TRUE"
    }

    KEY_PRESSES = {
        "KEY_SINGLE": "ID_ONE_CLICK_MOVE",
        "KEY_CONTINUE": "ID_CONTINUOUS_MOVE"
    }

    def __init__(self, panel):
        Blueprint.__init__(self, panel, FB())
        self.set_custom_size(FunctionBlueprint.SIZE)
        self.change_font(pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.get_rect().height * .13)))
        self.type_pressed = [False, None]
        self.type_selection = list()
        # MOVEMENT SPECIFIC
        self.orient_pressed = [False, None]
        self.orient_selection = list()
        self.direct_pressed = [False, None]
        self.direct_selection = list()
        self.keys_pressed = [False, None]
        self.keys_selection = list()

    def get_data(self):
        data = super().get_data()
        data[1] = StringUtils.get_string("ID_FUNCTION")
        data[2] = StringUtils.get_string(FunctionBlueprint.TYPE.get(self.get_blueprint().func_type))
        data[3] = StringUtils.get_string(FunctionBlueprint.ORIENTATION.get(self.get_blueprint().orientation))
        data[4] = StringUtils.get_string(FunctionBlueprint.DIRECTIONAL.get(self.get_blueprint().directional))
        data[5] = StringUtils.get_string(FunctionBlueprint.KEY_PRESSES.get(self.get_blueprint().key_press))
        return data

    def set_data(self, index, data):
        if index == 2:
            for key, value in FunctionBlueprint.TYPE.items():
                if data == StringUtils.get_string(value):
                    self.get_blueprint().func_type = key
        elif index == 3:
            for key, value in FunctionBlueprint.ORIENTATION.items():
                if data == StringUtils.get_string(value):
                    self.get_blueprint().orientation = key
        elif index == 4:
            for key, value in FunctionBlueprint.DIRECTIONAL.items():
                if data == StringUtils.get_string(value):
                    self.get_blueprint().directional = key
        elif index == 5:
            for key, value in FunctionBlueprint.KEY_PRESSES.items():
                if data == StringUtils.get_string(value):
                    self.get_blueprint().key_press = key
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
        self.type_pressed = [False, None]
        self.type_selection = list()
        self.orient_pressed = [False, None]
        self.orient_selection = list()
        self.direct_pressed = [False, None]
        self.direct_selection = list()
        self.keys_pressed = [False, None]
        self.keys_selection = list()

    def update_displayed_data(self, text):
        super().update_displayed_data(text)
