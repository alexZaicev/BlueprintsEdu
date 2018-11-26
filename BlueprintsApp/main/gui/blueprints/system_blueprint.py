from blueprints.system_blueprint import SystemBlueprint as SB
from gui.blueprints.blueprint import Blueprint
from utils.string_utils import StringUtils
from utils.gui_utils import Themes
import pygame as pg


class SystemBlueprint(Blueprint):
    SIZE = [.2, .15]

    def __init__(self, panel):
        Blueprint.__init__(self, panel, SB())
        self.set_custom_size(SystemBlueprint.SIZE)
        self.music_pressed = [False, None]
        self.music_selection = list()
        self.change_font(pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.get_rect().height * .17)))
        self.color_name = ""
        self.red, self.green, self.blue = 0, 0, 0

    def initialize(self, coords, size, blueprint, panel):
        super().initialize(coords, size, blueprint, panel)
        self.change_font(pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.get_rect().height * .17)))

    def reset_selection(self):
        self.music_pressed = [False, None]
        self.music_selection = list()

    def update_displayed_data(self, text):
        super().update_displayed_data(text)

    def add_color(self):
        rgb = (int(self.red), int(self.green), int(self.blue))
        if self.color_name not in self.get_blueprint().colors and \
            rgb not in self.get_blueprint().colors.values():
            self.get_blueprint().colors[self.color_name] = rgb
        # reset
        self.color_name = ""
        self.red, self.green, self.blue = 0, 0, 0

    def get_data(self):
        r = super().get_data()
        bp = self.get_blueprint()
        r[1] = StringUtils.get_string("ID_SYSTEM")
        r[2] = bp.size[0]
        r[3] = bp.size[1]
        r[4] = StringUtils.get_string(Blueprint.ENABLING_DICT.get(self.get_blueprint().music))
        r[5] = self.color_name
        r[6] = self.red
        r[7] = self.blue
        r[8] = self.green
        i = 1
        for k, v in bp.colors.items():
            r[8 + i] = "{} : {}".format(k.upper(), v)
            i += 1
        return r

    def set_data(self, index, data):
        if index == 2 or index == 3 or 5 < index < 9:
            if len(data) == 0:
                data = "0"

        if index == 2:
            temp = list(self.get_blueprint().size)
            temp[0] = data
            self.get_blueprint().size = temp
        elif index == 3:
            temp = list(self.get_blueprint().size)
            temp[1] = data
            self.get_blueprint().size = temp
        elif index == 4:
            for key, value in Blueprint.ENABLING_DICT.items():
                if data == StringUtils.get_string(value):
                    self.get_blueprint().music = key
        elif index == 5:
            self.color_name = data
        elif index == 6:
            self.red = data
        elif index == 7:
            self.blue = data
        elif index == 8:
            self.green = data
        elif index > 8:
            if len(data) == 2:
                self.get_blueprint().colors[data[0]] = data[1]
        super().set_data(index, data)
        self.update_displayed_data(self.font.render(self.get_blueprint().name,
                                                    True, Themes.DEFAULT_THEME.get("font")))



