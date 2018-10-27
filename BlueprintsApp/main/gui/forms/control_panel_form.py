from gui.forms.form import Form
from utils.gui_utils import Themes
from utils import logger_utils
import pygame as pg
from utils.string_utils import StringUtils


class ControlPanelForm(Form):

    def __init__(self, display, coords=None, size=None):
        Form.__init__(self, display, coords, size)
        self.__logger = logger_utils.get_logger(__name__)
        self.__bp = None

    def set_blueprint(self, bp):
        self.__bp = bp

    def draw_form(self):
        form_rect = self.get_rect()
        if (self.__bp is not None) and (self.__bp.focused):
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
        self.display_data(rect_txt)

    def display_data(self, banner):
        def __blit(font, text, text2, coords):
            t = font.render(text, True, Themes.DEFAULT_THEME.get("text_area_text"))
            r = t.get_rect()
            r.topleft = coords

            br = pg.Rect((0, 0),
                         (int(self.get_rect().width * .5), font.size(text2)[1]))
            br.topright = (int(self.get_rect().right - self.get_rect().width * .05), coords[1])

            t2 = font.render(text2, True, Themes.DEFAULT_THEME.get("text_area_text"))
            r2 = t.get_rect()
            r2.centery = br.centery
            r2.left = br.left * 1.1
            self.display.blit(t, r)
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("text_area_background"), br, 0)
            self.display.blit(t2, r2)

        if (self.__bp is not None) and (self.__bp.focused):
            dt = self.__bp.get_data()
            font = pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.get_rect().width * .05))
            margin = int(font.size("SOME_TEXT")[1] * .35)
            __blit(font, "{}:".format(StringUtils.get_string("ID_NAME")), dt.get("name"),
                   (int(self.get_rect().left + self.get_rect().width * .05), int(banner.bottom * 1.1)))
            __blit(font, "{}:".format(StringUtils.get_string("ID_TYPE")), dt.get("type"),
                   (int(self.get_rect().left + self.get_rect().width * .05), int(banner.bottom * 1.1 + margin + font.size(dt.get("name"))[1])))

    def check_form_events(self, event):
        super().check_form_events(event)
