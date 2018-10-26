from gui.forms.form import Form
from utils.gui_utils import Themes
from utils import logger_utils
import pygame as pg
from utils.string_utils import StringUtils
from gui.blueprints.attribute_blueprint import AttributeBlueprint


class BlueprintControlForm(Form):

    def __init__(self, display, coords=None, size=None):
        Form.__init__(self, display, coords, size)
        self.__logger = logger_utils.get_logger(__name__)
        self.__bps = list()

    def draw_form(self):
        if self.get_rect().collidepoint(pg.mouse.get_pos()) == 1:
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("panel_background"), self.get_rect(), 0)
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("selection_background"), self.get_rect(), 2)
        else:
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("panel_disabled"), self.get_rect(), 0)
        if len(self.__bps) > 0:
            for bp in self.__bps:
                pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("panel_front_light"), bp.get_rect(), 0)

    def check_form_events(self, event):
        super().check_form_events(event)

    def add_attribute(self):
        t = AttributeBlueprint(self.get_rect(), None)
        self.__bps.append(t)
