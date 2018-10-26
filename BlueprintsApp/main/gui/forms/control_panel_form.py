from gui.forms.form import Form
from utils.gui_utils import Themes
from utils import logger_utils
import pygame as pg
from utils.string_utils import StringUtils


class ControlPanelForm(Form):

    def __init__(self, display, coords=None, size=None):
        Form.__init__(self, display, coords, size)
        self.__logger = logger_utils.get_logger(__name__)
        self.__bp_focused = False

    def draw_form(self):
        form_rect = self.get_rect()
        if self.__bp_focused:
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("panel_background"), form_rect, 0)
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("selection_background"), form_rect, 2)
            pg.draw.rect(self.display, self.btn_apply.color, self.btn_apply.get_rect(), 0)
            self.display.blit(self.btn_apply.get_text(), self.btn_apply.get_text_rect())
            self.check_button_hover()
        else:
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("panel_disabled"), form_rect, 0)

        font = pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(form_rect.width * .08))
        txt = font.render(StringUtils.get_string("ID_CONTROL_PANEL"), True, Themes.DEFAULT_THEME.get("font"))
        rect_txt = txt.get_rect()
        rect_txt.topleft = (int(form_rect.topleft[0] * 1.015), int(form_rect.topleft[1] * 1.015))
        self.display.blit(txt, rect_txt)

    def check_form_events(self, event):
        super().check_form_events(event)
