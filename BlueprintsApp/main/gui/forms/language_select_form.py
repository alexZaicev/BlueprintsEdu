from gui.forms.form import Form
import pygame as pg
from utils.gui_utils import Themes
from utils.string_utils import StringUtils


class LanguageSelectForm(Form):

    def __init__(self, display, coords=None, size=None):
        Form.__init__(self, display, coords, size)

    def draw_form(self):
        super().draw_form()
        if self.visible:
            font = pg.font.Font(Themes.DEFAULT_THEME.get("banner_font_style"), int(self.size[1] * .07))
            txt = font.render(StringUtils.get_string("ID_LANGUAGE"), True, Themes.DEFAULT_THEME.get("font"))
            rect_txt = txt.get_rect()
            rect_txt.topleft = (int(self.coords[0] * 1.05), int(self.coords[1] * 1.05))
            # DRAWINGS
            self.display.blit(txt, rect_txt)

    def check_form_events(self, event):
        super().check_form_events(event)
