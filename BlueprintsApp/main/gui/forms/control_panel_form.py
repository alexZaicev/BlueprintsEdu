from gui.forms.form import Form
from utils.gui_utils import Themes
from utils import logger_utils
import pygame as pg
from utils.string_utils import StringUtils
from blueprints.blueprint import Blueprint
from pygame.locals import *
from utils.app_utils import Events
from gui.blueprints.attribute_blueprint import AttributeBlueprint
from gui.blueprints.character_blueprint import CharacterBlueprint
from blueprints import attribute_blueprint
from blueprints.attribute_blueprint import AttributeBlueprint as AB
from blueprints.function_blueprint import FunctionBlueprint as FB
from blueprints.sprite_blueprint import SpriteBlueprint as SB


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
        if (self.__bp is not None) and self.__bp.focused:
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
        for t in CharacterBlueprint.STATES:
            r = pg.Rect((self.__bp.state_pressed[1].left, int(
                self.__bp.state_pressed[1].top + self.__bp.state_pressed[1].height * pos)),
                        self.__bp.state_pressed[1].size)
            font = pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.get_rect().width * .05))
            t = StringUtils.get_string(CharacterBlueprint.STATES.get(t))
            txt = font.render(t, True, Themes.DEFAULT_THEME.get("text_area_text"))
            rt = txt.get_rect()
            rt.centery = r.centery
            rt.left = r.left * 1.1
            pos += 1
            self.__bp.state_selection.append([r, txt, rt, t])
        for s in self.__bp.state_selection:
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

            if self.__bp.get_blueprint().get_type() == Blueprint.TYPES.get("ATTRIBUTE"):
                # ATTRIBUTE RELATED INFORMATION
                self.draw_attribute_data(dt, pos, font, banner, margin)
            elif self.__bp.get_blueprint().get_type() == Blueprint.TYPES.get("FUNCTION"):
                # FUNCTION RELATED INFORMATION
                self.draw_function_data(dt, pos, font, banner, margin)
            elif self.__bp.get_blueprint().get_type() == Blueprint.TYPES.get("CHARACTER"):
                # CHARACTER RELATED INFORMATION
                self.draw_character_data(dt, pos, font, banner, margin)
            elif self.__bp.get_blueprint().get_type() == Blueprint.TYPES.get("SPRITE"):
                # SPRITE RELATED INFORMATION
                self.draw_sprite_data(dt, pos, font, banner, margin)
            self.ta_populated = True
            if self.boarder_rect is not None:
                pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("selection_boarder"), self.boarder_rect, 2)
            # DRAW ACTION RELATED WIDGETS
            if self.__bp.get_blueprint().get_type() == Blueprint.TYPES.get("ATTRIBUTE"):
                # DATA TYPE DROP DOWN
                if self.__bp.data_type_pressed[0]:
                    self.draw_attribute_data_type_selection()
            elif self.__bp.get_blueprint().get_type() == Blueprint.TYPES.get("FUNCTION"):
                pass
            elif self.__bp.get_blueprint().get_type() == Blueprint.TYPES.get("SPRITE"):
                pass
            elif self.__bp.get_blueprint().get_type() == Blueprint.TYPES.get("CHARACTER"):
                if self.__bp.state_pressed[0]:
                    self.draw_character_state_selection()

    def draw_attribute_data(self, data, pos, font, banner, margin):
        self.blit(font, "{}:".format(StringUtils.get_string("ID_DATA_TYPE")), data.get(2),
                  (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)))
        pos += 1
        self.blit(font, "{}:".format(StringUtils.get_string("ID_VALUE")), str(data.get(3)),
                  (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)))

    def draw_function_data(self, data, pos, font, banner, margin):
        # TODO implement method
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
                    self.__bp.reset_selection()
                    for ta in self.__tas:
                        if ta.collidepoint(event.pos) == 1:
                            self.boarder_rect = ta
                            found = True
                            if self.__tas.index(ta) == 2 and isinstance(self.__bp, AttributeBlueprint):
                                # DATA TYPE SELECTION
                                self.__bp.data_type_pressed = True, ta
                            elif self.__tas.index(ta) == 6 and isinstance(self.__bp, CharacterBlueprint):
                                self.__bp.state_pressed = True, ta
                            break
                    else:  # if break then not reachable
                        self.__bp.reset_selection()
                    if not found:
                        self.boarder_rect = None

        super().check_form_events(event)
        if self.__bp is not None:
            if self.__bp.get_blueprint().get_type() == Blueprint.TYPES.get("ATTRIBUTE"):
                # ATTRIBUTE specific events
                self.__attribute_events(event)
            elif self.__bp.get_blueprint().get_type() == Blueprint.TYPES.get("CHARACTER"):
                # CHARACTER specific events
                self.__character_events(event)
            elif self.__bp.get_blueprint().get_type() == Blueprint.TYPES.get("SPRITE"):
                # SPRITE specific events
                self.__sprite_events(event)
            elif self.__bp.get_blueprint().get_type() == Blueprint.TYPES.get("FUNCTION"):
                # FUNCTION specific events
                self.__function_event(event)

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
                    i = self.__tas.index(self.boarder_rect) - 2  # 2 = INDEX OF NAME AND TYPE TextAreas
                    if 0 <= i < len(al):
                        self.__bp.get_blueprint().remove_connection(al[i])
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
                    i = self.__tas.index(self.boarder_rect) - 2  # 2 = INDEX OF NAME AND TYPE TextAreas
                    if 0 <= i < len(al):
                        self.__bp.get_blueprint().remove_connection(al[i])
                        self.__tas.clear()
                        self.ta_populated = False
                        self.boarder_rect = None

    def __function_event(self, event):
        pass

    def int_try_parse(self, num):
        try:
            return True, int(num)
        except ValueError as ex:
            return False, num

    def float_try_parse(self, num):
        try:
            return True, float(num)
        except ValueError as ex:
            return False, num

    def __set_str(self, index, c):
        """Description: Method validates control panel input and sets data to
        the selected blueprint
        """

        def __write_str(data):
            if len(data) < 15:
                data += c
                self.__bp.set_data(index, data)

        dt = str(self.__bp.get_data().get(index))
        if dt is None:
            dt = ""
        if index == 3 and isinstance(self.__bp, AttributeBlueprint):  # value index
            if self.__bp.get_blueprint().get_data_type() == attribute_blueprint.NONE:
                self.__bp.set_data(index, StringUtils.get_string("ID_NONE"))
            elif self.__bp.get_blueprint().get_data_type() == attribute_blueprint.INT:
                dt += c
                if self.int_try_parse(dt)[0]:
                    self.__bp.set_data(index, int(dt))
                else:
                    self.__bp.set_data(index, "")
            elif self.__bp.get_blueprint().get_data_type() == attribute_blueprint.FLOAT:
                dt += c
                if self.float_try_parse(dt)[0]:
                    self.__bp.set_data(index, dt)
                else:
                    self.__bp.set_data(index, dt[:-1])
            elif self.__bp.get_blueprint().get_data_type() == attribute_blueprint.STRING:
                __write_str(dt)
            elif self.__bp.get_blueprint().get_data_type() == attribute_blueprint.CHAR:
                self.__bp.set_data(index, c)
        else:
            __write_str(dt)
