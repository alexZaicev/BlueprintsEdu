from gui.forms.form import Form
from utils.gui_utils import Themes
from utils import logger_utils
import pygame as pg
from utils.string_utils import StringUtils
from blueprints.blueprint import Blueprint
from pygame.locals import *
from utils.app_utils import Events
from gui.blueprints.attribute_blueprint import AttributeBlueprint


class ControlPanelForm(Form):

    def __init__(self, display, coords=None, size=None):
        Form.__init__(self, display, coords, size)
        self.__logger = logger_utils.get_logger(__name__)
        self.__bp = None
        self.ta_populated = False
        self.__tas = list()
        self.boarder_rect = None

    def set_blueprint(self, bp):
        self.__bp = bp

    def draw_form(self):
        form_rect = self.get_rect()
        if (self.__bp is not None) and (self.__bp.focused):
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("panel_background"), form_rect, 0)
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("selection_background"), form_rect, 2)
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
            text = str(text)
            text2 = str(text2)
            t = font.render(text, True, Themes.DEFAULT_THEME.get("text_area_text"))
            r = t.get_rect()
            r.topleft = coords

            br = pg.Rect((0, 0),
                         (int(self.get_rect().width * .5), font.size(text2)[1]))
            br.topright = (int(self.get_rect().right - self.get_rect().width * .05), coords[1])
            if not self.ta_populated:
                self.__tas.append(br)

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
            __blit(font, "{}:".format(StringUtils.get_string("ID_NAME")), dt.get(0),
                   (int(self.get_rect().left + self.get_rect().width * .05), int(banner.bottom * 1.1)))
            __blit(font, "{}:".format(StringUtils.get_string("ID_TYPE")), dt.get(1),
                   (int(self.get_rect().left + self.get_rect().width * .05), int(banner.bottom * 1.1 + margin + font.size(dt.get(1))[1])))

            if self.__bp.get_blueprint().get_type() == Blueprint.TYPES.get("ATTRIBUTE"):
                # ATTRIBUTE RELATED INFORMATION
                # TODO implement drop down for data type selection
                __blit(font, "{}:".format(StringUtils.get_string("ID_DATA_TYPE")), dt.get(2),
                       (int(self.get_rect().left + self.get_rect().width * .05), int(banner.bottom * 1.1 + 2*(margin + font.size(dt.get(1))[1]))))
                __blit(font, "{}:".format(StringUtils.get_string("ID_VALUE")), dt.get(3),
                       (int(self.get_rect().left + self.get_rect().width * .05), int(banner.bottom * 1.1 + 3*(margin + font.size(str(dt.get(1)))[1]))))
            elif self.__bp.get_blueprint().get_type() == Blueprint.TYPES.get("FUNCTION"):
                # FUNCTION RELATED INFORMATION
                pass
            elif self.__bp.get_blueprint().get_type() == Blueprint.TYPES.get("CHARACTER"):
                # CHARACTER RELATED INFORMATION
                pass
            elif self.__bp.get_blueprint().get_type() == Blueprint.TYPES.get("SPRITE"):
                # SPRITE RELATED INFORMATION
                pass
            self.ta_populated = True
            if self.boarder_rect is not None:
                pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("selection_boarder"), self.boarder_rect, 2)
            if self.__bp.data_type_pressed[0]:
                self.draw_data_type_selection()

    def check_form_events(self, event):
        super().check_form_events(event)
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 and self.__bp is not None:
                #self.check_data_type_selection(event.pos)
                for ls in self.__bp.data_type_selection:
                    if ls[0].collidepoint(event.pos) == 1:
                        self.__bp.set_data(2, ls[3])
                        self.__bp.data_type_selection.clear()
                        self.__bp.data_type_pressed = False, None
                        break
                else: # if not found
                    found = False
                    for ta in self.__tas:
                        if ta.collidepoint(event.pos) == 1:
                            self.boarder_rect = ta
                            found = True
                            if self.__tas.index(ta) == 2:
                                # DATA TYPE SELECTION
                                if not self.__bp.data_type_pressed[0]:
                                    self.__bp.data_type_pressed = True, ta
                            break
                    else:  # if break then not reachable
                        self.__bp.data_type_pressed = False, None
                    if not found:
                        self.boarder_rect = None
        elif event.type == KEYDOWN:
            if self.__bp is not None:
                c = Events.get_char(event.key)
                index = [
                    i for i in range(0, len(self.__tas), 1) if self.__tas[i].topleft == self.boarder_rect.topleft
                ][0]
                if c == Events.SPECIAL_KEYS.get("DELETE"):
                    self.__bp.set_data(index, "")
                elif c == Events.SPECIAL_KEYS.get("BACKSPACE"):
                    dt = self.__bp.get_data().get(index)
                    if len(dt) > 0:
                        dt = dt[:-1]
                        self.__bp.set_data(index, dt)
                elif c == Events.SPECIAL_KEYS.get("UNREGISTERED"):
                    # ALL UNREGISTERED KEYS ARE SKIPPED
                    pass
                else:
                    self.__set_str(index, c)

    def draw_data_type_selection(self):
        self.__bp.data_type_selection.clear()
        pos = 1
        for t in AttributeBlueprint.DATA_TYPE:
            r = pg.Rect((self.__bp.data_type_pressed[1].left, int(
                self.__bp.data_type_pressed[1].top + self.__bp.data_type_pressed[1].height*pos)),
                self.__bp.data_type_pressed[1].size)
            font = pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.get_rect().width * .05))
            t = StringUtils.get_string(AttributeBlueprint.DATA_TYPE.get(t))
            txt = font.render(t, True, Themes.DEFAULT_THEME.get("text_area_text"))
            rt = txt.get_rect()
            rt.centery = r.centery
            rt.left = r.left * 1.1
            pos += 1
            self.__bp.data_type_selection.append([r, txt, rt, t])
        for s in self.__bp.data_type_selection:
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("text_area_background"), s[0], 0)
            self.display.blit(s[1], s[2])

    def check_data_type_selection(self, pos):
        if self.__bp is not None and self.__bp.data_type_pressed[0]:
            for ls in self.__bp.data_type_selection:
                if ls[0].collidepoint(pos) == 1:
                    self.__logger.debug("DATA TYPE {} ".format(ls[3]))
                    self.__bp.set_data(2, ls[3])
                    break

    def __set_str(self, index, c):
        dt = self.__bp.get_data().get(index)
        # TODO implement value validation for valid int/float/char
        if dt is None:
            dt = ""
        if len(dt) < 15:
            dt += c
            self.__bp.set_data(index, dt)
