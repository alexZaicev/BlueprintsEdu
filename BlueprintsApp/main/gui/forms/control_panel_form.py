import pygame as pg
from pygame.locals import *

from blueprints.attribute_blueprint import AttributeBlueprint as AB
from blueprints.blueprint import Blueprint as BP
from blueprints.function_blueprint import FunctionBlueprint as FB
from blueprints.sprite_blueprint import SpriteBlueprint as SB
from gui.blueprints.attribute_blueprint import AttributeBlueprint
from gui.blueprints.blueprint import Blueprint
from gui.blueprints.character_blueprint import CharacterBlueprint
from gui.blueprints.function_blueprint import FunctionBlueprint
from gui.blueprints.sprite_blueprint import SpriteBlueprint
from gui.blueprints.system_blueprint import SystemBlueprint
from gui.forms.form import Form
from utils import logger_utils
from utils.app_utils import Events
from utils.gui_utils import Themes
from utils.string_utils import StringUtils


class ControlPanelForm(Form):

    def __init__(self, display, coords=None, size=None):
        Form.__init__(self, display, coords, size)
        self.__logger = logger_utils.get_logger(__name__)
        self.__bp = None
        self.ta_populated = False
        self.__tas = list()
        self.boarder_rect = None

    def set_blueprint(self, bp):
        if self.__bp is not None:
            self.__bp.reset_selection()
        self.__tas.clear()
        self.ta_populated = False
        self.__bp = bp

    def update_form(self, coords=None, size=None):
        super().update_form(coords, size)

    def draw_form(self):
        form_rect = self.get_rect()
        if self.__bp is not None and self.__bp.focused:
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

    def draw_attribute_data_type_selection(self):
        self.__bp.data_type_selection.clear()
        pos = 1
        for t in AttributeBlueprint.DATA_TYPE:
            r = pg.Rect((self.__bp.data_type_pressed[1].left, int(
                self.__bp.data_type_pressed[1].top + self.__bp.data_type_pressed[1].height * pos)),
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

    def draw_character_state_selection(self):
        self.__bp.state_selection.clear()
        pos = 1
        for t in Blueprint.CONDITIONAL_DICT:
            r = pg.Rect((self.__bp.state_pressed[1].left, int(
                self.__bp.state_pressed[1].top + self.__bp.state_pressed[1].height * pos)),
                        self.__bp.state_pressed[1].size)
            font = pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.get_rect().width * .05))
            t = StringUtils.get_string(Blueprint.CONDITIONAL_DICT.get(t))
            txt = font.render(t, True, Themes.DEFAULT_THEME.get("text_area_text"))
            rt = txt.get_rect()
            rt.centery = r.centery
            rt.left = r.left * 1.1
            pos += 1
            self.__bp.state_selection.append([r, txt, rt, t])
        for s in self.__bp.state_selection:
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("text_area_background"), s[0], 0)
            self.display.blit(s[1], s[2])

    def draw_functions_type_selection(self):
        self.__bp.type_selection.clear()
        pos = 1
        for t in FunctionBlueprint.TYPE:
            r = pg.Rect((self.__bp.type_pressed[1].left, int(
                self.__bp.type_pressed[1].top + self.__bp.type_pressed[1].height * pos)),
                        self.__bp.type_pressed[1].size)
            font = pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.get_rect().width * .05))
            t = StringUtils.get_string(FunctionBlueprint.TYPE.get(t))
            txt = font.render(t, True, Themes.DEFAULT_THEME.get("text_area_text"))
            rt = txt.get_rect()
            rt.centery = r.centery
            rt.left = r.left * 1.1
            pos += 1
            self.__bp.type_selection.append([r, txt, rt, t])
        for s in self.__bp.type_selection:
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("text_area_background"), s[0], 0)
            self.display.blit(s[1], s[2])

    def draw_functions_orientation_selection(self):
        self.__bp.orient_selection.clear()
        pos = 1
        for t in FunctionBlueprint.ORIENTATION:
            r = pg.Rect((self.__bp.orient_pressed[1].left, int(
                self.__bp.orient_pressed[1].top + self.__bp.orient_pressed[1].height * pos)),
                        self.__bp.orient_pressed[1].size)
            font = pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.get_rect().width * .05))
            t = StringUtils.get_string(FunctionBlueprint.ORIENTATION.get(t))
            txt = font.render(t, True, Themes.DEFAULT_THEME.get("text_area_text"))
            rt = txt.get_rect()
            rt.centery = r.centery
            rt.left = r.left * 1.1
            pos += 1
            self.__bp.orient_selection.append([r, txt, rt, t])
        for s in self.__bp.orient_selection:
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("text_area_background"), s[0], 0)
            self.display.blit(s[1], s[2])

    def draw_functions_direction_selection(self):
        self.__bp.direct_selection.clear()
        pos = 1
        for t in Blueprint.CONDITIONAL_DICT:
            r = pg.Rect((self.__bp.direct_pressed[1].left, int(
                self.__bp.direct_pressed[1].top + self.__bp.direct_pressed[1].height * pos)),
                        self.__bp.direct_pressed[1].size)
            font = pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.get_rect().width * .05))
            t = StringUtils.get_string(Blueprint.CONDITIONAL_DICT.get(t))
            txt = font.render(t, True, Themes.DEFAULT_THEME.get("text_area_text"))
            rt = txt.get_rect()
            rt.centery = r.centery
            rt.left = r.left * 1.1
            pos += 1
            self.__bp.direct_selection.append([r, txt, rt, t])
        for s in self.__bp.direct_selection:
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("text_area_background"), s[0], 0)
            self.display.blit(s[1], s[2])

    def draw_functions_key_press_selection(self):
        self.__bp.keys_selection.clear()
        pos = 1
        for t in FunctionBlueprint.KEY_PRESSES:
            r = pg.Rect((self.__bp.keys_pressed[1].left, int(
                self.__bp.keys_pressed[1].top + self.__bp.keys_pressed[1].height * pos)),
                        self.__bp.keys_pressed[1].size)
            font = pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.get_rect().width * .05))
            t = StringUtils.get_string(FunctionBlueprint.KEY_PRESSES.get(t))
            txt = font.render(t, True, Themes.DEFAULT_THEME.get("text_area_text"))
            rt = txt.get_rect()
            rt.centery = r.centery
            rt.left = r.left * 1.1
            pos += 1
            self.__bp.keys_selection.append([r, txt, rt, t])
        for s in self.__bp.keys_selection:
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("text_area_background"), s[0], 0)
            self.display.blit(s[1], s[2])

    def draw_system_color_selection(self):
        self.__bp.color_selection.clear()
        pos = 1
        colors = self.__bp.get_blueprint().colors
        if len(colors) > 0:
            for t in colors:
                r = pg.Rect((self.__bp.color_pressed[1].left, int(
                    self.__bp.color_pressed[1].top + self.__bp.color_pressed[1].height * pos)),
                            self.__bp.color_pressed[1].size)
                font = pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.get_rect().width * .05))
                txt = font.render(t, True, Themes.DEFAULT_THEME.get("text_area_text"))
                rt = txt.get_rect()
                rt.centery = r.centery
                rt.left = r.left * 1.1
                pos += 1
                self.__bp.color_selection.append([r, txt, rt, t])
            for s in self.__bp.color_selection:
                pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("text_area_background"), s[0], 0)
                self.display.blit(s[1], s[2])

    def draw_system_music_selection(self):
        self.__bp.music_selection.clear()
        pos = 1
        for t in Blueprint.ENABLING_DICT:
            r = pg.Rect((self.__bp.music_pressed[1].left, int(
                self.__bp.music_pressed[1].top + self.__bp.music_pressed[1].height * pos)),
                        self.__bp.music_pressed[1].size)
            font = pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.get_rect().width * .05))
            t = StringUtils.get_string(Blueprint.ENABLING_DICT.get(t))
            txt = font.render(t, True, Themes.DEFAULT_THEME.get("text_area_text"))
            rt = txt.get_rect()
            rt.centery = r.centery
            rt.left = r.left * 1.1
            pos += 1
            self.__bp.music_selection.append([r, txt, rt, t])
        for s in self.__bp.music_selection:
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("text_area_background"), s[0], 0)
            self.display.blit(s[1], s[2])

    def blit(self, font, text, text2, coords, header=True):
        if text is not None:
            text = str(text)
            t = font.render(text, True, Themes.DEFAULT_THEME.get("text_area_text"))
            r = t.get_rect()
            r.topleft = coords
            if text2 is None and not header:
                br = pg.Rect((int(r.left * .72), r.top), (int(r.width * 1.44), r.height))
                if not self.ta_populated:
                    self.__tas.append(br)
                pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("panel_background"), br, 0)

            self.display.blit(t, r)

        if text2 is not None:
            br = pg.Rect((0, 0),
                         (int(self.get_rect().width * .5), font.size(text2)[1]))
            br.topright = (int(self.get_rect().right - self.get_rect().width * .05), coords[1])
            if not self.ta_populated:
                self.__tas.append(br)
            t2 = font.render(text2, True, Themes.DEFAULT_THEME.get("text_area_text"))
            r2 = t2.get_rect()
            r2.centery = br.centery
            r2.left = br.left * 1.1

            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("text_area_background"), br, 0)
            self.display.blit(t2, r2)

    def display_data(self, banner):
        if self.__bp is not None and self.__bp.focused:
            dt = self.__bp.get_data()
            pos = 2
            font = pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.get_rect().width * .05))
            margin = int(font.size("SOME_TEXT")[1] * .35) + font.size(dt.get(1))[1]
            # DRAW GENERIC BLUEPRINT DATA
            self.blit(font, "{}:".format(StringUtils.get_string("ID_NAME")), dt.get(0),
                      (int(self.get_rect().left + self.get_rect().width * .05), int(banner.bottom * 1.1)))
            self.blit(font, "{}:".format(StringUtils.get_string("ID_TYPE")), dt.get(1),
                      (int(self.get_rect().left + self.get_rect().width * .05),
                       int(banner.bottom * 1.1 + margin)))

            if self.__bp.get_blueprint().get_type() == BP.TYPES.get("ATTRIBUTE"):
                # ATTRIBUTE RELATED INFORMATION
                self.draw_attribute_data(dt, pos, font, banner, margin)
            elif self.__bp.get_blueprint().get_type() == BP.TYPES.get("FUNCTION"):
                # FUNCTION RELATED INFORMATION
                self.draw_function_data(dt, pos, font, banner, margin)
            elif self.__bp.get_blueprint().get_type() == BP.TYPES.get("CHARACTER"):
                # CHARACTER RELATED INFORMATION
                self.draw_character_data(dt, pos, font, banner, margin)
            elif self.__bp.get_blueprint().get_type() == BP.TYPES.get("SPRITE"):
                # SPRITE RELATED INFORMATION
                self.draw_sprite_data(dt, pos, font, banner, margin)
            elif self.__bp.get_blueprint().get_type() == BP.TYPES.get("SYSTEM"):
                # SYSTEM (BOARD) RELATED INFORMATION
                self.draw_system_data(dt, pos, font, banner, margin)
            self.ta_populated = True
            if self.boarder_rect is not None:
                pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("selection_boarder"), self.boarder_rect, 2)
            # DRAW ACTION RELATED WIDGETS
            if self.__bp.get_blueprint().get_type() == BP.TYPES.get("ATTRIBUTE"):
                # DATA TYPE DROP DOWN
                if self.__bp.data_type_pressed[0]:
                    self.draw_attribute_data_type_selection()
            elif self.__bp.get_blueprint().get_type() == BP.TYPES.get("FUNCTION"):
                if self.__bp.type_pressed[0]:
                    self.draw_functions_type_selection()
                elif self.__bp.orient_pressed[0]:
                    self.draw_functions_orientation_selection()
                elif self.__bp.direct_pressed[0]:
                    self.draw_functions_direction_selection()
                elif self.__bp.keys_pressed[0]:
                    self.draw_functions_key_press_selection()
            elif self.__bp.get_blueprint().get_type() == BP.TYPES.get("SPRITE"):
                pass
            elif self.__bp.get_blueprint().get_type() == BP.TYPES.get("CHARACTER"):
                if self.__bp.state_pressed[0]:
                    self.draw_character_state_selection()
            elif self.__bp.get_blueprint().get_type() == BP.TYPES.get("SYSTEM"):
                if self.__bp.music_pressed[0]:
                    self.draw_system_music_selection()
                elif self.__bp.color_pressed[0]:
                    self.draw_system_color_selection()

    def draw_system_data(self, data, pos, font, banner, margin):
        self.blit(font, "{}:".format(StringUtils.get_string("ID_WIDTH")), str(data.get(2)),
                  (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)))
        pos += 1
        self.blit(font, "{}:".format(StringUtils.get_string("ID_HEIGHT")), str(data.get(3)),
                  (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)))
        pos += 1
        self.blit(font, "{}:".format(StringUtils.get_string("ID_MUSIC")), data.get(4),
                  (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)))
        pos += 1
        self.blit(font, "{}:".format(StringUtils.get_string("ID_SOUND")), data.get(5),
                  (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)))
        pos += 1
        self.blit(font, "{}:".format(StringUtils.get_string("ID_BACKGROUND")), data.get(6),
                  (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)))
        pos += 1
        self.blit(font, "{}:".format(StringUtils.get_string("ID_COLOR_ID")), data.get(7),
                  (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)))
        pos += 1
        # custom RBG input areas
        size = list(font.size("000"))
        size[0] *= 1.6
        offset = self.get_rect().width * .02
        # RED
        txt = font.render("Red:", True, Themes.DEFAULT_THEME.get("text_area_text"))
        rect_txt = txt.get_rect()
        rect_txt.topleft = (int(self.get_rect().left + self.get_rect().width * .05),
                            int(banner.bottom * 1.1 + pos * margin))
        self.display.blit(txt, rect_txt)
        ta = pg.Rect((int(rect_txt.right + offset), int(rect_txt.top)), size)
        pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("text_area_background"), ta, 0)
        if not self.ta_populated:
            self.__tas.append(ta)
        # GREEN
        txt = font.render("Green:", True, Themes.DEFAULT_THEME.get("text_area_text"))
        rect_txt = txt.get_rect()
        rect_txt.topleft = (int(ta.right + ta.width * .4),
                            int(banner.bottom * 1.1 + pos * margin))
        self.display.blit(txt, rect_txt)
        ta = pg.Rect((int(rect_txt.right + offset), int(rect_txt.top)), size)
        pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("text_area_background"), ta, 0)
        if not self.ta_populated:
            self.__tas.append(ta)
        # BLUE
        txt = font.render("Blue:", True, Themes.DEFAULT_THEME.get("text_area_text"))
        rect_txt = txt.get_rect()
        rect_txt.topleft = (int(ta.right + ta.width * .4),
                            int(banner.bottom * 1.1 + pos * margin))
        self.display.blit(txt, rect_txt)
        ta = pg.Rect((int(rect_txt.right + offset), int(rect_txt.top)), size)
        pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("text_area_background"), ta, 0)
        if not self.ta_populated:
            self.__tas.append(ta)

        for i in range(8, 11, 1):
            txt = font.render(str(data.get(i)), True, Themes.DEFAULT_THEME.get("text_area_text"))
            rect_txt = txt.get_rect()
            rect_txt.center = self.__tas[i].center
            self.display.blit(txt, rect_txt)
        pos += 1
        # ADD BUTTON
        txt = font.render(StringUtils.get_string("ID_ADD"), True, Themes.DEFAULT_THEME.get("font"))
        size = font.size(StringUtils.get_string("ID_ADD"))
        btn_add = pg.Rect((0, 0), (int(size[0] * 1.6), size[1]))
        btn_add.topright = (ta.right, int(banner.bottom * 1.1 + pos * margin))
        pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("button_dark"), btn_add, 0)
        rect_txt = txt.get_rect()
        rect_txt.center = btn_add.center
        self.display.blit(txt, rect_txt)
        if not self.ta_populated:
            self.__tas.append(btn_add)
        pos += 1
        # DRAW EXISTING COLORS
        if len(self.__bp.get_blueprint().colors) > 0:
            for k, v in self.__bp.get_blueprint().colors.items():
                r = pg.Rect((int(self.get_rect().left + self.get_rect().width * .03),
                             int(banner.bottom * 1.1 + pos * margin + margin * .3)),
                            (self.size[0] * .03, self.size[0] * .03))
                pg.draw.rect(self.display, v, r, 0)
                self.blit(font, "{}:".format(k), str(v),
                          (int(self.get_rect().left + self.get_rect().width * .08),
                           int(banner.bottom * 1.1 + pos * margin)), header=False)
                pos += 1

    def draw_attribute_data(self, data, pos, font, banner, margin):
        self.blit(font, "{}:".format(StringUtils.get_string("ID_DATA_TYPE")), data.get(2),
                  (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)))
        pos += 1
        self.blit(font, "{}:".format(StringUtils.get_string("ID_VALUE")), str(data.get(3)),
                  (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)))

    def draw_function_data(self, data, pos, font, banner, margin):
        self.blit(font, "{}:".format(StringUtils.get_string("ID_FUNCTION")), data.get(2),
                  (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)))
        pos += 1

        if StringUtils.get_string("ID_MOVEMENT") == StringUtils.get_string(
                FunctionBlueprint.TYPE.get(self.__bp.get_blueprint().func_type)):
            self.blit(font, "{}:".format(StringUtils.get_string("ID_ORIENTATION")), data.get(3),
                      (int(self.get_rect().left + self.get_rect().width * .05),
                       int(banner.bottom * 1.1 + pos * margin)))
            pos += 1
            self.blit(font, "{}:".format(StringUtils.get_string("ID_DIRECTIONAL")), data.get(4),
                      (int(self.get_rect().left + self.get_rect().width * .05),
                       int(banner.bottom * 1.1 + pos * margin)))
            pos += 1
            self.blit(font, "{}:".format(StringUtils.get_string("ID_ON_KEY_PRESS")), data.get(5),
                      (int(self.get_rect().left + self.get_rect().width * .05),
                       int(banner.bottom * 1.1 + pos * margin)))
            pos += 1
        elif StringUtils.get_string("ID_CUSTOM") == StringUtils.get_string(
                FunctionBlueprint.TYPE.get(self.__bp.get_blueprint().func_type)):
            # TODO implement
            pass

    def draw_sprite_data(self, data, pos, font, banner, margin):
        s = pos = pos + 1
        if len(self.__bp.get_blueprint().attributes) > 0:
            self.blit(font, "{}".format(StringUtils.get_string("ID_ATTRIBUTES")), None,
                      (int(self.get_rect().left + self.get_rect().width * .08),
                       int(banner.bottom * 1.1 + pos * margin)))
            pos += 1
            for bp in self.__bp.get_blueprint().attributes:
                if isinstance(bp, AB):
                    self.blit(font, "{}  ::  {}".format(bp.get_data_type(), bp.get_value()),
                              None,
                              (int(self.get_rect().left + self.get_rect().width * .12),
                               int(banner.bottom * 1.1 + pos * margin)), header=False)
                    pos += 1

            r = pg.Rect(
                (int(self.get_rect().left + self.get_rect().width * .05), int(banner.bottom * 1.1 + s * margin)),
                (int(self.get_rect().width * .90), int((pos - s) * margin)))
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("selection_boarder"), r, 1)
            s = pos = pos + 1
        if len(self.__bp.get_blueprint().functions) > 0:
            self.blit(font, "{}".format(StringUtils.get_string("ID_FUNCTIONS")), None,
                      (int(self.get_rect().left + self.get_rect().width * .08),
                       int(banner.bottom * 1.1 + pos * margin)))
            pos += 1
            for bp in self.__bp.get_blueprint().functions:
                if isinstance(bp, FB):
                    self.blit(font, "{}()".format(bp.name), None,
                              (int(self.get_rect().left + self.get_rect().width * .12),
                               int(banner.bottom * 1.1 + pos * margin)), header=False)
                    pos += 1
            r = pg.Rect(
                (int(self.get_rect().left + self.get_rect().width * .05), int(banner.bottom * 1.1 + s * margin)),
                (int(self.get_rect().width * .90), int((pos - s) * margin)))
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("selection_boarder"), r, 1)

    def draw_character_data(self, data, pos, font, banner, margin):
        self.blit(font, "{}:".format(StringUtils.get_string("ID_POS_X")), str(data[2]),
                  (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin))
                  )
        s = pos = pos + 1
        self.blit(font, "{}:".format(StringUtils.get_string("ID_POS_Y")), str(data[3]),
                  (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin))
                  )
        s = pos = pos + 1
        self.blit(font, "{}:".format(StringUtils.get_string("ID_WIDTH")), str(data[4]),
                  (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin))
                  )
        s = pos = pos + 1
        self.blit(font, "{}:".format(StringUtils.get_string("ID_HEIGHT")), str(data[5]),
                  (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin))
                  )
        s = pos = pos + 1
        self.blit(font, "{}:".format(StringUtils.get_string("ID_ALIVE")), str(data[6]),
                  (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin))
                  )
        s = pos = pos + 1
        if len(self.__bp.get_blueprint().attributes) > 0:
            self.blit(font, "{}".format(StringUtils.get_string("ID_ATTRIBUTES")), None,
                      (int(self.get_rect().left + self.get_rect().width * .08),
                       int(banner.bottom * 1.1 + pos * margin)))
            pos += 1
            for bp in self.__bp.get_blueprint().attributes:
                if isinstance(bp, AB):
                    self.blit(font, "{}  ::  {}".format(bp.get_data_type(), bp.get_value()),
                              None,
                              (int(self.get_rect().left + self.get_rect().width * .12),
                               int(banner.bottom * 1.1 + pos * margin)), header=False)
                    pos += 1

            r = pg.Rect(
                (int(self.get_rect().left + self.get_rect().width * .05), int(banner.bottom * 1.1 + s * margin)),
                (int(self.get_rect().width * .90), int((pos - s) * margin)))
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("selection_boarder"), r, 1)

            s = pos = pos + 1
        if len(self.__bp.get_blueprint().functions) > 0:
            self.blit(font, "{}".format(StringUtils.get_string("ID_FUNCTIONS")), None,
                      (int(self.get_rect().left + self.get_rect().width * .08),
                       int(banner.bottom * 1.1 + pos * margin)))
            pos += 1
            for bp in self.__bp.get_blueprint().functions:
                if isinstance(bp, FB):
                    self.blit(font, "{}()".format(bp.name), None,
                              (int(self.get_rect().left + self.get_rect().width * .12),
                               int(banner.bottom * 1.1 + pos * margin)), header=False)
                    pos += 1

            r = pg.Rect(
                (int(self.get_rect().left + self.get_rect().width * .05), int(banner.bottom * 1.1 + s * margin)),
                (int(self.get_rect().width * .90), int((pos - s) * margin)))
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("selection_boarder"), r, 1)

            s = pos = pos + 1
        if len(self.__bp.get_blueprint().sprites) > 0:
            self.blit(font, "{}".format(StringUtils.get_string("ID_SPRITES")), None,
                      (int(self.get_rect().left + self.get_rect().width * .08),
                       int(banner.bottom * 1.1 + pos * margin)))
            pos += 1
            for bp in self.__bp.get_blueprint().sprites:
                if isinstance(bp, SB):
                    self.blit(font, "{}".format(bp.name), None,
                              (int(self.get_rect().left + self.get_rect().width * .12),
                               int(banner.bottom * 1.1 + pos * margin)), header=False)
                    pos += 1

            r = pg.Rect(
                (int(self.get_rect().left + self.get_rect().width * .05), int(banner.bottom * 1.1 + s * margin)),
                (int(self.get_rect().width * .90), int((pos - s) * margin)))
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("selection_boarder"), r, 1)

    def check_form_events(self, event):

        def __check_textarea_selection():
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    found = False
                    for ta in self.__tas:
                        if ta.collidepoint(event.pos) == 1:
                            self.boarder_rect = ta
                            found = True
                            if self.__tas.index(ta) == 2 and isinstance(self.__bp, AttributeBlueprint):
                                # DATA TYPE SELECTION
                                self.__bp.data_type_pressed = True, ta
                                break
                            elif self.__tas.index(ta) == 6 and isinstance(self.__bp, CharacterBlueprint):
                                self.__bp.state_pressed = True, ta
                                break
                            elif isinstance(self.__bp, FunctionBlueprint):
                                if self.__tas.index(ta) == 2:
                                    if not self.__bp.orient_pressed[0] and not self.__bp.direct_pressed[0] and \
                                            not self.__bp.keys_pressed[0]:
                                        self.__bp.type_pressed = True, ta
                                        break
                                elif self.__tas.index(ta) == 3:
                                    if not self.__bp.type_pressed[0] and not self.__bp.direct_pressed[0] and \
                                            not self.__bp.keys_pressed[0]:
                                        self.__bp.orient_pressed = True, ta
                                        break
                                elif self.__tas.index(ta) == 4:
                                    if not self.__bp.orient_pressed[0] and not self.__bp.type_pressed[0] and \
                                            not self.__bp.keys_pressed[0]:
                                        self.__bp.direct_pressed = True, ta
                                        break
                                elif self.__tas.index(ta) == 5:
                                    if not self.__bp.orient_pressed[0] and not self.__bp.direct_pressed[0] and \
                                            not self.__bp.type_pressed[0]:
                                        self.__bp.keys_pressed = True, ta
                                        break
                            elif isinstance(self.__bp, SystemBlueprint):
                                if self.__tas.index(ta) == 4:
                                    self.__bp.music_pressed = True, ta
                                    break
                                elif self.__tas.index(ta) == 6:
                                    self.__bp.color_pressed = True, ta
                                    break
                                elif self.__tas.index(ta) == 11:
                                    self.__bp.add_color()
                                    self.ta_populated = False
                                    self.__tas.clear()
                                    break
                    else:
                        # statement not reached if break
                        self.__bp.reset_selection()
                    if not found:
                        self.boarder_rect = None

        super().check_form_events(event)
        if self.__bp is not None:
            if self.__bp.get_blueprint().get_type() == BP.TYPES.get("ATTRIBUTE"):
                # ATTRIBUTE specific events
                self.__attribute_events(event)
            elif self.__bp.get_blueprint().get_type() == BP.TYPES.get("CHARACTER"):
                # CHARACTER specific events
                self.__character_events(event)
            elif self.__bp.get_blueprint().get_type() == BP.TYPES.get("SPRITE"):
                # SPRITE specific events
                self.__sprite_events(event)
            elif self.__bp.get_blueprint().get_type() == BP.TYPES.get("FUNCTION"):
                # FUNCTION specific events
                self.__function_event(event)
            elif self.__bp.get_blueprint().get_type() == BP.TYPES.get("SYSTEM"):
                # FUNCTION specific events
                self.__system_event(event)

            __check_textarea_selection()

            if event.type == KEYDOWN or event.type == KEYUP:
                if self.boarder_rect is not None and self.ta_populated:
                    c = Events.get_char(event.key, event.type)
                    if event.type == KEYDOWN:
                        index = [
                            i for i in range(0, len(self.__tas), 1) if
                            self.__tas[i].topleft == self.boarder_rect.topleft
                        ][0]
                        if c == Events.SPECIAL_KEYS.get("DELETE"):
                            if isinstance(self.__bp, AttributeBlueprint):
                                if index == 3:
                                    if self.__bp.get_blueprint().get_data_type() != AB.NONE:
                                        self.__bp.set_data(index, "")
                                else:
                                    self.__bp.set_data(index, "")
                            else:
                                self.__bp.set_data(index, "")
                        elif c == Events.SPECIAL_KEYS.get("BACKSPACE"):
                            dt = str(self.__bp.get_data().get(index))
                            if len(dt) > 0:
                                dt = dt[:-1]
                                self.__bp.set_data(index, dt)
                        elif c == Events.SPECIAL_KEYS.get("UNREGISTERED"):
                            # ALL UNREGISTERED KEYS ARE SKIPPED
                            pass
                        elif isinstance(c, str):
                            self.__set_str(index, c)

    def __system_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.__bp.music_pressed[0]:
                    for ls in self.__bp.music_selection:
                        if ls[0].collidepoint(event.pos) == 1:
                            self.__bp.set_data(4, ls[3])
                            self.__bp.reset_selection()
                            break
                elif self.__bp.color_pressed[0]:
                    for ls in self.__bp.color_selection:
                        if ls[0].collidepoint(event.pos) == 1:
                            self.__bp.set_data(6, ls[3])
                            self.__bp.reset_selection()
                            break
        elif event.type == KEYDOWN:
            c = Events.get_char(event.key, event_type=event.type)
            if c == Events.SPECIAL_KEYS.get("DELETE"):
                if self.ta_populated and self.boarder_rect is not None:
                    i = self.__tas.index(self.boarder_rect) - 11
                    if 0 < i < (len(self.__tas) - 11):
                        j, key = 1, None
                        for k, v in self.__bp.get_blueprint().colors.items():
                            if j == i:
                                key = k
                                break
                            else:
                                j += 1
                        self.__bp.get_blueprint().colors.pop(key)
                        self.__tas.clear()
                        self.ta_populated, self.boarder_rect = False, None
                        if self.__bp.get_blueprint().board_color not in self.__bp.get_blueprint().colors.keys():
                            self.__bp.get_blueprint().board_color = StringUtils.get_string("ID_NONE")

    def __attribute_events(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                for ls in self.__bp.data_type_selection:
                    if ls[0].collidepoint(event.pos) == 1:
                        self.__bp.set_data(2, ls[3])
                        self.__bp.reset_selection()
                        if self.__bp.get_blueprint().get_data_type() == 'none':
                            self.__bp.get_blueprint().set_value(StringUtils.get_string("ID_NONE"))
                        else:
                            self.__bp.get_blueprint().set_value("")
                        break

    def __character_events(self, event):
        if event.type == KEYDOWN:
            c = Events.get_char(event.key, event_type=event.type)
            if c == Events.SPECIAL_KEYS.get("DELETE"):
                if self.ta_populated and self.boarder_rect is not None:
                    # DELETE connection from character
                    al = list()
                    al.extend(self.__bp.get_blueprint().attributes)
                    al.extend(self.__bp.get_blueprint().functions)
                    al.extend(self.__bp.get_blueprint().sprites)
                    i = self.__tas.index(self.boarder_rect)
                    if 6 < i < len(self.__tas):
                        self.__bp.get_blueprint().remove_connection(al[i - 7])
                        self.__tas.clear()
                        self.ta_populated = False
                        self.boarder_rect = None
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                for ls in self.__bp.state_selection:
                    if ls[0].collidepoint(event.pos) == 1:
                        self.__bp.set_data(6, ls[3])
                        self.__bp.reset_selection()
                        break

    def __sprite_events(self, event):
        if event.type == KEYDOWN:
            c = Events.get_char(event.key, event_type=event.type)
            if c == Events.SPECIAL_KEYS.get("DELETE"):
                if self.ta_populated and self.boarder_rect is not None:
                    # DELETE connection from character
                    al = list()
                    al.extend(self.__bp.get_blueprint().attributes)
                    al.extend(self.__bp.get_blueprint().functions)
                    i = self.__tas.index(self.boarder_rect)
                    if 1 < i < len(self.__tas):
                        self.__bp.get_blueprint().remove_connection(al[i - 2])
                        self.__tas.clear()
                        self.ta_populated = False
                        self.boarder_rect = None

    def __function_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.__bp.type_pressed[0]:
                    for ls in self.__bp.type_selection:
                        if ls[0].collidepoint(event.pos) == 1:
                            self.__bp.set_data(2, ls[3])
                            break
                elif self.__bp.orient_pressed[0]:
                    for ls in self.__bp.orient_selection:
                        if ls[0].collidepoint(event.pos) == 1:
                            self.__bp.set_data(3, ls[3])
                            break
                elif self.__bp.direct_pressed[0]:
                    for ls in self.__bp.direct_selection:
                        if ls[0].collidepoint(event.pos) == 1:
                            self.__bp.set_data(4, ls[3])
                            break
                elif self.__bp.keys_pressed[0]:
                    for ls in self.__bp.keys_selection:
                        if ls[0].collidepoint(event.pos) == 1:
                            self.__bp.set_data(5, ls[3])
                            break

    def int_try_parse(self, num):
        try:
            if " " in num:
                raise ValueError()
            else:
                return True, int(num)
        except ValueError as ex:
            return False, num

    def float_try_parse(self, num):
        try:
            if " " in num:
                raise ValueError()
            else:
                return True, float(num)
        except ValueError as ex:
            return False, num

    def __set_str(self, index, c):
        """Description: Method validates control panel input and sets data to
        the selected blueprint field
        """

        def __write_str(data):
            if len(data) < 15:
                self.__bp.set_data(index, data)

        dt = str(self.__bp.get_data().get(index))
        if dt is None:
            dt = ""
        dt += c
        # check blueprint specific input
        if isinstance(self.__bp, AttributeBlueprint):
            if index == 3:
                if self.__bp.get_blueprint().get_data_type() == AB.NONE:
                    __write_str(StringUtils.get_string("ID_NONE"))
                elif self.__bp.get_blueprint().get_data_type() == AB.INT:
                    if self.int_try_parse(dt)[0]:
                        __write_str(dt)
                    else:
                        __write_str(dt[:-1])
                elif self.__bp.get_blueprint().get_data_type() == AB.FLOAT:
                    if self.float_try_parse(dt)[0]:
                        __write_str(dt)
                    else:
                        __write_str(dt[:-1])
                elif self.__bp.get_blueprint().get_data_type() == AB.STRING:
                    __write_str(dt)
                elif self.__bp.get_blueprint().get_data_type() == AB.CHAR:
                    __write_str(c)
            else:
                __write_str(dt)
        elif isinstance(self.__bp, FunctionBlueprint):
            pass
        elif isinstance(self.__bp, CharacterBlueprint):
            if 2 <= index <= 5:
                if self.int_try_parse(dt)[0]:
                    __write_str(dt)
                else:
                    __write_str(dt[:-1])
        elif isinstance(self.__bp, SpriteBlueprint):
            pass
        elif isinstance(self.__bp, SystemBlueprint):
            if index == 2 or index == 3 or 7 < index < 11:
                if self.int_try_parse(dt)[0]:
                    for c in dt:
                        if c == "0":
                            dt = dt[1:]
                        else:
                            break
                    if 7 < index < 11:
                        if len(dt) < 4 and int(dt) < 256:
                            __write_str(dt)
                    else:
                        __write_str(dt)
                else:
                    __write_str(dt[:-1])
            else:
                __write_str(dt)
