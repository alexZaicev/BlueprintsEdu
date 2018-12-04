import pygame as pg
from pygame.locals import *

from blueprints.attribute_blueprint import AttributeBlueprint as AB
from blueprints.blueprint import Blueprint as BP
from blueprints.system_blueprint import SystemBlueprint as SYS_BP
from gui.blueprints.attribute_blueprint import AttributeBlueprint
from gui.blueprints.blueprint import Blueprint
from gui.blueprints.function_blueprint import FunctionBlueprint
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
        self.__displayed_data = list()
        self.__counter = 0
        self.__max_number_boxes = 0
        self.__drop_down_activated = False

    def find_max_number_boxes(self, size):
        temp, num = size, 0
        while temp < self.get_rect().height:
            self.__logger.debug("HEIGHT: {}, TEMP: {}".format(self.get_rect().height, temp))
            num += 1
            temp += size
        return num

    def set_blueprint(self, bp):
        if self.__bp is not None:
            self.__bp.reset_selection()
        self.__tas.clear()
        self.ta_populated = False
        self.__bp = bp
        self.__max_number_boxes = 0
        self.__drop_down_activated = False

    def update_form(self, coords=None, size=None):
        super().update_form(coords, size)

    def draw_form(self):
        form_rect = self.get_rect()
        if self.__bp is not None and self.__bp.focused:
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("panel_background"), form_rect, 0)
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("selection_background"), form_rect, 2)
        else:
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("panel_disabled"), form_rect, 0)
        self.display_data()

    def draw_drop_down_selection(self, selection, data, box, assignment=True, scrolling=False, size=None, counter=None):
        """Description: Generic drop down drawer.

        :param selection: Array that contains drop down data
        :param data: Source of the drop down data
        :param box: Pressed text area rectangle
        :param assignment: If text value requires assignment
        :param scrolling: Drop down scrolling functionality
        :param size: Drop down size
        :param counter: Scrolling counter to determine what data to show
        :return: Array of generated drop down items
        """

        def generate_data(value):
            rect = pg.Rect((box.left, int(box.top + box.height * pos)), box.size)
            font = pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.get_rect().width * .05))
            if assignment:
                value = StringUtils.get_string(data.get(value))
            txt = font.render(value, True, Themes.DEFAULT_THEME.get("text_area_text"))
            rect_text = txt.get_rect()
            rect_text.centery = rect.centery
            rect_text.left = rect.left * 1.1
            return rect, txt, rect_text, value

        selection.clear()
        pos = 1
        if len(data) > 0:
            i = 0
            for item in data:
                if scrolling:
                    if counter <= i < len(data):
                        if (i - counter) < size:
                            selection.append(generate_data(item))
                            pos += 1
                        else:
                            break
                    i += 1
                else:
                    selection.append(generate_data(item))
                    pos += 1
            for item in selection:
                pos = pg.mouse.get_pos()
                if item[0].collidepoint(pos):
                    pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("selected_drop_down_item"), item[0], 0)
                else:
                    pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("drop_down_item"), item[0], 0)
                self.display.blit(item[1], item[2])
        return selection

    def get_data_row(self, font, top_left, text_1=None, text_2=None):
        """Description: Creates a row of data to display in control panel

        :param font: Pygame font object
        :param top_left: Row starting coordinates
        :param text_1: Row header string
        :param text_2: Text area string value
        :return: Array of row data to display
        """
        txt, rect_txt, box = None, None, None
        if text_1 is not None:
            txt = font.render(text_1, True, Themes.DEFAULT_THEME.get("text_area_text"))
            rect_txt = txt.get_rect()
            rect_txt.topleft = top_left
            data_1 = (txt, rect_txt)
        else:
            data_1 = None

        if text_2 is not None:
            box = pg.Rect((0, 0),
                          (int(self.get_rect().width * .5), font.size(text_2)[1]))
            self.__logger.debug(font.size(text_2)[1])
            box.topright = (int(self.get_rect().right - self.get_rect().width * .05), top_left[1])
            txt = font.render(text_2, True, Themes.DEFAULT_THEME.get("text_area_text"))
            rect_txt = txt.get_rect()
            rect_txt.centery = box.centery
            rect_txt.left = box.left * 1.1
            data_2 = (box, Themes.DEFAULT_THEME.get("text_area_background"))
            data_3 = (txt, rect_txt)
        else:
            data_2, data_3 = None, None

        if not self.ta_populated and box is not None:
            self.__tas.append(box)

        return data_1, data_2, data_3

    def gather_data(self, banner):
        """Description: Function populates blueprint properties

        :param banner:
        :return: Boolean status of successful data gathering
        """
        self.__displayed_data.clear()
        data = self.__bp.get_data()
        pos = 0 - self.__counter
        font = pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.get_rect().width * .05))
        margin = int(font.size("SOME_TEXT")[1] * .35) + font.size(data.get(1))[1]

        self.__displayed_data.append(self.get_data_row(
            font, (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)), "{}:".format(StringUtils.get_string("ID_NAME")),
            data.get(0)))
        pos += 1

        if self.__max_number_boxes < 1:
            self.__max_number_boxes = self.find_max_number_boxes(margin)

        self.__displayed_data.append(self.get_data_row(
            font, (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)), "{}:".format(StringUtils.get_string("ID_TYPE")),
            data.get(1)))
        pos += 1
        func_calls = {
            BP.TYPES.get("ATTRIBUTE"): self.draw_attribute_data,
            BP.TYPES.get("CHARACTER"): self.draw_character_data,
            BP.TYPES.get("SPRITE"): self.draw_sprite_data,
            BP.TYPES.get("FUNCTION"): self.draw_function_data,
            BP.TYPES.get("SYSTEM"): self.draw_system_data
        }
        try:
            func_calls[self.__bp.get_blueprint().get_type()](
                data, pos, font, banner, margin
            )
        except KeyError:
            return False

        return True

    def draw_attribute_drop_down(self):
        if self.__bp.data_type_pressed[0]:
            self.__bp.data_type_selection = self.draw_drop_down_selection(
                selection=self.__bp.data_type_selection,
                data=AttributeBlueprint.DATA_TYPE,
                box=self.__bp.data_type_pressed[1])

    def draw_character_drop_down(self):
        if self.__bp.state_pressed[0]:
            # self.draw_character_state_selection()
            self.__bp.state_selection = self.draw_drop_down_selection(
                selection=self.__bp.state_selection,
                data=Blueprint.CONDITIONAL_DICT,
                box=self.__bp.state_pressed[1]
            )
        elif self.__bp.color_scheme_1_pressed[0]:
            self.__bp.color_scheme_1_selection = self.draw_drop_down_selection(
                selection=self.__bp.color_scheme_1_selection,
                data=self.__bp.parent.colors,
                box=self.__bp.color_scheme_1_pressed[1],
                assignment=False,
                scrolling=True,
                size=5,
                counter=self.__bp.color_scheme_1_counter
            )
        elif self.__bp.color_scheme_2_pressed[0]:
            self.__bp.color_scheme_2_selection = self.draw_drop_down_selection(
                selection=self.__bp.color_scheme_2_selection,
                data=self.__bp.parent.colors,
                box=self.__bp.color_scheme_2_pressed[1],
                assignment=False,
                scrolling=True,
                size=5,
                counter=self.__bp.color_scheme_2_counter
            )
        elif self.__bp.color_scheme_3_pressed[0]:
            self.__bp.color_scheme_3_selection = self.draw_drop_down_selection(
                selection=self.__bp.color_scheme_3_selection,
                data=self.__bp.parent.colors,
                box=self.__bp.color_scheme_3_pressed[1],
                assignment=False,
                scrolling=True,
                size=5,
                counter=self.__bp.color_scheme_3_counter
            )

    def draw_sprite_drop_down(self):
        pass

    def draw_function_drop_down(self):
        if self.__bp.type_pressed[0]:
            self.__bp.type_selection = self.draw_drop_down_selection(
                selection=self.__bp.type_selection,
                data=FunctionBlueprint.TYPE,
                box=self.__bp.type_pressed[1]
            )
        elif self.__bp.orient_pressed[0]:
            self.__bp.orient_selection = self.draw_drop_down_selection(
                selection=self.__bp.orient_selection,
                data=FunctionBlueprint.ORIENTATION,
                box=self.__bp.orient_pressed[1]
            )
        elif self.__bp.direct_pressed[0]:
            self.__bp.direct_selection = self.draw_drop_down_selection(
                selection=self.__bp.direct_selection,
                data=Blueprint.CONDITIONAL_DICT,
                box=self.__bp.direct_pressed[1]
            )
        elif self.__bp.keys_pressed[0]:
            self.__bp.keys_selection = self.draw_drop_down_selection(
                selection=self.__bp.keys_selection,
                data=FunctionBlueprint.KEY_PRESSES,
                box=self.__bp.keys_pressed[1]
            )

    def draw_system_drop_down(self):
        if self.__bp.music_pressed[0]:
            self.__bp.music_selection = self.draw_drop_down_selection(
                selection=self.__bp.music_selection,
                data=Blueprint.ENABLING_DICT,
                box=self.__bp.music_pressed[1]
            )
        elif self.__bp.color_pressed[0]:
            self.__bp.color_selection = self.draw_drop_down_selection(
                selection=self.__bp.color_selection,
                data=self.__bp.get_blueprint().colors,
                box=self.__bp.color_pressed[1],
                assignment=False,
                scrolling=True,
                size=5,
                counter=self.__bp.color_counter
            )
        elif self.__bp.music_effect_pressed[0]:
            self.__bp.music_effect_selection = self.draw_drop_down_selection(
                selection=self.__bp.music_effect_selection,
                data=SYS_BP.SOUND_EFFECTS,
                box=self.__bp.music_effect_pressed[1],
                assignment=True,
                scrolling=True,
                size=5,
                counter=self.__bp.music_effect_counter
            )

    def display_data(self):
        if self.__bp is not None and self.__bp.focused:
            banner = pg.Rect(
                self.get_rect().topleft, (self.get_rect().width, 20)
            )
            if self.gather_data(banner):
                for data_1, data_2, data_3 in self.__displayed_data:
                    if data_2[0].top >= banner.bottom:
                        if data_1 is not None:
                            self.display.blit(data_1[0], data_1[1])
                        if data_2 is not None:
                            pg.draw.rect(self.display, data_2[1], data_2[0], 0)
                        if data_3 is not None:
                            self.display.blit(data_3[0], data_3[1])
                self.ta_populated = True

                drop_down_calls = {
                    BP.TYPES.get("ATTRIBUTE"): self.draw_attribute_drop_down,
                    BP.TYPES.get("CHARACTER"): self.draw_character_drop_down,
                    BP.TYPES.get("SPRITE"): self.draw_sprite_drop_down,
                    BP.TYPES.get("FUNCTION"): self.draw_function_drop_down,
                    BP.TYPES.get("SYSTEM"): self.draw_system_drop_down
                }
                try:
                    drop_down_calls[self.__bp.get_blueprint().get_type()]()
                except KeyError:
                    self.__logger.error("Failed to draw drop down of unknown blueprint type {}"
                                        .format(self.__bp.get_blueprint().get_type()))
                if self.boarder_rect is not None:
                    pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("selection_boarder"), self.boarder_rect, 2)

    def draw_system_data(self, data, pos, font, banner, margin):
        self.__displayed_data.append(self.get_data_row(
            font, (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)), "{}:".format(StringUtils.get_string("ID_WIDTH")),
            str(data.get(2))))
        pos += 1
        self.__displayed_data.append(self.get_data_row(
            font, (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)), "{}:".format(StringUtils.get_string("ID_HEIGHT")),
            str(data.get(3))))
        pos += 1
        self.__displayed_data.append(self.get_data_row(
            font, (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)), "{}:".format(StringUtils.get_string("ID_MUSIC")),
            str(data.get(4))))
        pos += 1
        self.__displayed_data.append(self.get_data_row(
            font, (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)), "{}:".format(StringUtils.get_string("ID_SOUND")),
            str(data.get(5))))
        pos += 1
        self.__displayed_data.append(self.get_data_row(
            font, (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)), "{}:".format(StringUtils.get_string("ID_BACKGROUND")),
            str(data.get(6))))
        pos += 1
        self.__displayed_data.append(self.get_data_row(
            font, (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)), "{}:".format(StringUtils.get_string("ID_COLOR_ID")),
            str(data.get(7))))
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
        ta = pg.Rect((int(rect_txt.right + offset), int(rect_txt.top)), size)
        if not self.ta_populated:
            self.__tas.append(ta)
        data_1 = (txt, rect_txt)
        data_2 = (ta, Themes.DEFAULT_THEME.get("text_area_background"))

        txt = font.render(str(data.get(8)), True, Themes.DEFAULT_THEME.get("text_area_text"))
        rect_txt = txt.get_rect()
        rect_txt.center = ta.center

        data_3 = (txt, rect_txt)

        self.__displayed_data.append(
            (data_1, data_2, data_3)
        )

        # GREEN
        txt = font.render("Green:", True, Themes.DEFAULT_THEME.get("text_area_text"))
        rect_txt = txt.get_rect()
        rect_txt.topleft = (int(ta.right + ta.width * .4),
                            int(banner.bottom * 1.1 + pos * margin))

        ta = pg.Rect((int(rect_txt.right + offset), int(rect_txt.top)), size)
        if not self.ta_populated:
            self.__tas.append(ta)
        data_1 = (txt, rect_txt)
        data_2 = (ta, Themes.DEFAULT_THEME.get("text_area_background"))

        txt = font.render(str(data.get(9)), True, Themes.DEFAULT_THEME.get("text_area_text"))
        rect_txt = txt.get_rect()
        rect_txt.center = ta.center

        data_3 = (txt, rect_txt)
        self.__displayed_data.append(
            (data_1, data_2, data_3)
        )

        # BLUE
        txt = font.render("Blue:", True, Themes.DEFAULT_THEME.get("text_area_text"))
        rect_txt = txt.get_rect()
        rect_txt.topleft = (int(ta.right + ta.width * .4),
                            int(banner.bottom * 1.1 + pos * margin))
        ta = pg.Rect((int(rect_txt.right + offset), int(rect_txt.top)), size)
        if not self.ta_populated:
            self.__tas.append(ta)
        data_1 = (txt, rect_txt)
        data_2 = (ta, Themes.DEFAULT_THEME.get("text_area_background"))

        txt = font.render(str(data.get(10)), True, Themes.DEFAULT_THEME.get("text_area_text"))
        rect_txt = txt.get_rect()
        rect_txt.center = ta.center

        data_3 = (txt, rect_txt)
        self.__displayed_data.append(
            (data_1, data_2, data_3)
        )

        pos += 1
        # ADD BUTTON
        size = font.size(StringUtils.get_string("ID_ADD"))
        btn_add = pg.Rect((0, 0), (int(size[0] * 1.6), size[1]))
        btn_add.topright = (ta.right, int(banner.bottom * 1.1 + pos * margin))
        txt = font.render(StringUtils.get_string("ID_ADD"), True, Themes.DEFAULT_THEME.get("font"))
        rect_txt = txt.get_rect()
        rect_txt.center = btn_add.center
        if not self.ta_populated:
            self.__tas.append(btn_add)
        data_2 = (btn_add, Themes.DEFAULT_THEME.get("button_dark"))
        data_3 = (txt, rect_txt)

        self.__displayed_data.append((None, data_2, data_3))
        pos += 1
        for k, v in self.__bp.get_blueprint().colors.items():
            self.__displayed_data.append(
                self.get_data_row(font, (int(self.get_rect().left + self.get_rect().width * .08),
                                         int(banner.bottom * 1.1 + pos * margin)),
                                  "{}:".format(k), str(v)))
            pos += 1

    def draw_attribute_data(self, data, pos, font, banner, margin):
        self.__displayed_data.append(self.get_data_row(
            font, (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)), "{}:".format(StringUtils.get_string("ID_DATA_TYPE")),
            data.get(2)))
        pos += 1
        self.__displayed_data.append(self.get_data_row(
            font, (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)), "{}:".format(StringUtils.get_string("ID_VALUE")),
            str(data.get(3))))
        pos += 1

    def draw_function_data(self, data, pos, font, banner, margin):
        self.__displayed_data.append(self.get_data_row(
            font, (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)), "{}:".format(StringUtils.get_string("ID_FUNCTION")),
            data.get(2)))
        pos += 1

        if StringUtils.get_string("ID_MOVEMENT") == StringUtils.get_string(
                FunctionBlueprint.TYPE.get(self.__bp.get_blueprint().func_type)):
            self.__displayed_data.append(self.get_data_row(
                font, (int(self.get_rect().left + self.get_rect().width * .05),
                       int(banner.bottom * 1.1 + pos * margin)), "{}:".format(StringUtils.get_string("ID_ORIENTATION")),
                data.get(3)))
            pos += 1
            self.__displayed_data.append(self.get_data_row(
                font, (int(self.get_rect().left + self.get_rect().width * .05),
                       int(banner.bottom * 1.1 + pos * margin)), "{}:".format(StringUtils.get_string("ID_DIRECTIONAL")),
                data.get(4)))
            pos += 1
            self.__displayed_data.append(self.get_data_row(
                font, (int(self.get_rect().left + self.get_rect().width * .05),
                       int(banner.bottom * 1.1 + pos * margin)),
                "{}:".format(StringUtils.get_string("ID_ON_KEY_PRESS")),
                data.get(5)))
            pos += 1
        elif StringUtils.get_string("ID_CUSTOM") == StringUtils.get_string(
                FunctionBlueprint.TYPE.get(self.__bp.get_blueprint().func_type)):
            # TODO implement
            pass

    def draw_sprite_data(self, data, pos, font, banner, margin):
        # TODO re-implement method based on US - 36
        pass

    def draw_character_data(self, data, pos, font, banner, margin):
        self.__displayed_data.append(self.get_data_row(
            font, (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)),
            "{}:".format(StringUtils.get_string("ID_POS_X")),
            str(data.get(2))))
        pos += 1
        self.__displayed_data.append(self.get_data_row(
            font, (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)),
            "{}:".format(StringUtils.get_string("ID_POS_Y")),
            str(data.get(3))))
        pos += 1
        self.__displayed_data.append(self.get_data_row(
            font, (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)),
            "{}:".format(StringUtils.get_string("ID_WIDTH")),
            str(data.get(4))))
        pos += 1
        self.__displayed_data.append(self.get_data_row(
            font, (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)),
            "{}:".format(StringUtils.get_string("ID_HEIGHT")),
            str(data.get(5))))
        pos += 1
        self.__displayed_data.append(self.get_data_row(
            font, (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)),
            "{}:".format(StringUtils.get_string("ID_ALIVE")),
            str(data.get(6))))
        pos += 1
        self.__displayed_data.append(self.get_data_row(
            font, (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)),
            "{}:".format(StringUtils.get_string("ID_BODY_COLOR")),
            str(data.get(10))))
        pos += 1
        self.__displayed_data.append(self.get_data_row(
            font, (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)),
            "{}:".format(StringUtils.get_string("ID_TYRE_COLOR")),
            str(data.get(11))))
        pos += 1
        self.__displayed_data.append(self.get_data_row(
            font, (int(self.get_rect().left + self.get_rect().width * .05),
                   int(banner.bottom * 1.1 + pos * margin)),
            "{}:".format(StringUtils.get_string("ID_WINDOW_COLOR")),
            str(data.get(12))))
        pos += 1
        # TODO re-implement method based on US - 36

    def attribute_box_selection(self, box):
        if self.__tas.index(box) == 2:
            self.__bp.data_type_pressed = True, box
            return True
        return False

    def character_box_selection(self, box):
        if self.__tas.index(box) == 6:
            if not self.__bp.color_scheme_1_pressed[0] and \
                    not self.__bp.color_scheme_2_pressed[0] and \
                    not self.__bp.color_scheme_3_pressed[0]:
                self.__bp.state_pressed = True, box
                return True
        elif self.__tas.index(box) == 7:
            if not self.__bp.state_pressed[0] and \
                    not self.__bp.color_scheme_2_pressed[0] and \
                    not self.__bp.color_scheme_3_pressed[0]:
                self.__bp.color_scheme_1_pressed = True, box
                return True
        elif self.__tas.index(box) == 8:
            if not self.__bp.color_scheme_1_pressed[0] and \
                    not self.__bp.state_pressed[0] and \
                    not self.__bp.color_scheme_3_pressed[0]:
                self.__bp.color_scheme_2_pressed = True, box
                return True
        elif self.__tas.index(box) == 9:
            if not self.__bp.color_scheme_1_pressed[0] and \
                    not self.__bp.color_scheme_2_pressed[0] and \
                    not self.__bp.state_pressed[0]:
                self.__bp.color_scheme_3_pressed = True, box
                return True
        return False

    def sprite_box_selection(self, box):
        return False

    def function_box_selection(self, box):
        if self.__tas.index(box) == 2:
            if not self.__bp.orient_pressed[0] and not self.__bp.direct_pressed[0] and \
                    not self.__bp.keys_pressed[0]:
                self.__bp.type_pressed = True, box
                return True
        elif self.__tas.index(box) == 3:
            if not self.__bp.type_pressed[0] and not self.__bp.direct_pressed[0] and \
                    not self.__bp.keys_pressed[0]:
                self.__bp.orient_pressed = True, box
                return True
        elif self.__tas.index(box) == 4:
            if not self.__bp.orient_pressed[0] and not self.__bp.type_pressed[0] and \
                    not self.__bp.keys_pressed[0]:
                self.__bp.direct_pressed = True, box
                return True
        elif self.__tas.index(box) == 5:
            if not self.__bp.orient_pressed[0] and not self.__bp.direct_pressed[0] and \
                    not self.__bp.type_pressed[0]:
                self.__bp.keys_pressed = True, box
                return True
        return False

    def system_box_selection(self, box):
        if self.__tas.index(box) == 4:
            if not self.__bp.music_effect_pressed[0] and not self.__bp.color_pressed[0]:
                self.__bp.music_pressed = True, box
                return True
        elif self.__tas.index(box) == 5:
            if not self.__bp.music_pressed[0] and not self.__bp.color_pressed[0]:
                self.__bp.music_effect_pressed = True, box
                return True
        elif self.__tas.index(box) == 6:
            if not self.__bp.music_effect_pressed[0] and not self.__bp.music_pressed[0]:
                self.__bp.color_pressed = True, box
                return True
        elif self.__tas.index(box) == 11:
            self.__bp.add_color()
            self.ta_populated = False
            self.__tas.clear()
            self.boarder_rect = None
            return True
        return False

    def __check_panel_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if (event.button == 4 or event.button == 5) and not self.__drop_down_activated:
                if self.get_rect().collidepoint(event.pos):
                    if event.button == 4:
                        self.__counter -= 1
                    elif event.button == 5 and len(self.__displayed_data) > self.__max_number_boxes:
                        self.__counter += 1
                    if self.__counter < 0:
                        self.__counter = 0
                    elif len(self.__displayed_data) >= self.__max_number_boxes and \
                            (self.__counter > len(self.__displayed_data) - self.__max_number_boxes):
                        self.__counter = len(self.__displayed_data) - self.__max_number_boxes
                    self.ta_populated = False
                    self.boarder_rect = None
                    self.__tas.clear()

    def check_form_events(self, event):

        def __check_box_selection():
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.boarder_rect = None
                    for ta in self.__tas:
                        if ta.collidepoint(event.pos) == 1:
                            self.boarder_rect = ta
                            box_selection_calls = {
                                BP.TYPES.get("ATTRIBUTE"): self.attribute_box_selection,
                                BP.TYPES.get("CHARACTER"): self.character_box_selection,
                                BP.TYPES.get("SPRITE"): self.sprite_box_selection,
                                BP.TYPES.get("FUNCTION"): self.function_box_selection,
                                BP.TYPES.get("SYSTEM"): self.system_box_selection
                            }
                            try:
                                self.__drop_down_activated = box_selection_calls[self.__bp.get_blueprint().get_type()](
                                    ta)
                            except KeyError:
                                self.__drop_down_activated = False
                            if self.__drop_down_activated:
                                break
                    else:
                        # statement not reached if break
                        self.__drop_down_activated = False
                        self.__bp.reset_selection()

        super().check_form_events(event)
        if self.__bp is not None:
            self.__check_panel_event(event)
            events_calls = {
                BP.TYPES.get("ATTRIBUTE"): self.__attribute_events,
                BP.TYPES.get("CHARACTER"): self.__character_events,
                BP.TYPES.get("SPRITE"): self.__sprite_events,
                BP.TYPES.get("FUNCTION"): self.__function_events,
                BP.TYPES.get("SYSTEM"): self.__system_events
            }
            try:
                events_calls[self.__bp.get_blueprint().get_type()](event)
            except KeyError:
                pass

            __check_box_selection()

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

    def __handle_system_scrolling(self, button):
        if self.__bp.color_pressed[0]:
            if button == 4:
                self.__bp.color_counter -= 1
            elif button == 5 and len(self.__bp.get_blueprint().colors) > 5:
                self.__bp.color_counter += 1
            if self.__bp.color_counter < 0:
                self.__bp.color_counter = 0
            elif len(self.__bp.get_blueprint().colors) > 5 and (
                    self.__bp.color_counter > len(self.__bp.get_blueprint().colors) - 5):
                self.__bp.color_counter = len(self.__bp.get_blueprint().colors) - 5
        elif self.__bp.music_effect_pressed[0]:
            if button == 4:
                self.__bp.music_effect_counter -= 1
            elif button == 5 and len(SYS_BP.SOUND_EFFECTS) > 5:
                self.__bp.music_effect_counter += 1
            if self.__bp.music_effect_counter < 0:
                self.__bp.music_effect_counter = 0
            elif len(SYS_BP.SOUND_EFFECTS) > 5 and (
                    self.__bp.music_effect_counter > len(SYS_BP.SOUND_EFFECTS) - 5):
                self.__bp.music_effect_counter = len(SYS_BP.SOUND_EFFECTS) - 5

    def __handle_character_scrolling(self, button):
        if self.__bp.color_scheme_1_pressed[0]:
            if button == 4:
                self.__bp.color_scheme_1_counter -= 1
            elif button == 5 and len(self.__bp.parent.colors) > 5:
                self.__bp.color_scheme_1_counter += 1
            if self.__bp.color_scheme_1_counter < 0:
                self.__bp.color_scheme_1_counter = 0
            elif len(self.__bp.parent.colors) > 5 and (
                    self.__bp.color_scheme_1_counter > len(self.__bp.parent.colors) - 5):
                self.__bp.color_scheme_1_counter = len(self.__bp.parent.colors) - 5
        elif self.__bp.color_scheme_2_pressed[0]:
            if button == 4:
                self.__bp.color_scheme_2_counter -= 1
            elif button == 5 and len(self.__bp.parent.colors) > 5:
                self.__bp.color_scheme_2_counter += 1
            if self.__bp.color_scheme_2_counter < 0:
                self.__bp.color_scheme_2_counter = 0
            elif len(self.__bp.parent.colors) > 5 and (
                    self.__bp.color_scheme_2_counter > len(self.__bp.parent.colors) - 5):
                self.__bp.color_scheme_2_counter = len(self.__bp.parent.colors) - 5
        elif self.__bp.color_scheme_3_pressed[0]:
            if button == 4:
                self.__bp.color_scheme_3_counter -= 1
            elif button == 5 and len(self.__bp.parent.colors) > 5:
                self.__bp.color_scheme_3_counter += 1
            if self.__bp.color_scheme_3_counter < 0:
                self.__bp.color_scheme_3_counter = 0
            elif len(self.__bp.parent.colors) > 5 and (
                    self.__bp.color_scheme_3_counter > len(self.__bp.parent.colors) - 5):
                self.__bp.color_scheme_3_counter = len(self.__bp.parent.colors) - 5

    def __system_events(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.__bp.music_pressed[0]:
                    for ls in self.__bp.music_selection:
                        if ls[0].collidepoint(event.pos) == 1:
                            self.__bp.set_data(4, ls[3])
                            break
                elif self.__bp.color_pressed[0]:
                    for ls in self.__bp.color_selection:
                        if ls[0].collidepoint(event.pos) == 1:
                            self.__bp.set_data(6, ls[3])
                            break
                elif self.__bp.music_effect_pressed[0]:
                    for ls in self.__bp.music_effect_selection:
                        if ls[0].collidepoint(event.pos) == 1:
                            self.__bp.set_data(5, ls[3])
                            break
            elif event.button == 4 or event.button == 5:
                self.__handle_system_scrolling(event.button)
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
                        if self.__counter > 0:
                            self.__counter -= 1
                        if self.__bp.get_blueprint().board_color not in self.__bp.get_blueprint().colors.keys():
                            self.__bp.get_blueprint().board_color = StringUtils.get_string("ID_NONE")

    def __attribute_events(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.__bp.data_type_pressed[0]:
                    for ls in self.__bp.data_type_selection:
                        if ls[0].collidepoint(event.pos) == 1:
                            self.__bp.set_data(2, ls[3])
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
                if self.__bp.state_pressed[0]:
                    for ls in self.__bp.state_selection:
                        if ls[0].collidepoint(event.pos) == 1:
                            self.__bp.set_data(6, ls[3])
                            break
                elif self.__bp.color_scheme_1_pressed[0]:
                    for ls in self.__bp.color_scheme_1_selection:
                        if ls[0].collidepoint(event.pos) == 1:
                            self.__bp.set_data(10, ls[3])
                            break
                elif self.__bp.color_scheme_2_pressed[0]:
                    for ls in self.__bp.color_scheme_2_selection:
                        if ls[0].collidepoint(event.pos) == 1:
                            self.__bp.set_data(11, ls[3])
                            break
                elif self.__bp.color_scheme_3_pressed[0]:
                    for ls in self.__bp.color_scheme_3_selection:
                        if ls[0].collidepoint(event.pos) == 1:
                            self.__bp.set_data(12, ls[3])
                            break
            elif event.button == 4 or event.button == 5:
                self.__handle_character_scrolling(event.button)

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

    def __function_events(self, event):
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

    @staticmethod
    def int_try_parse(num):
        try:
            if " " in num:
                raise ValueError()
            else:
                return True, int(num)
        except ValueError as ex:
            return False, num

    @staticmethod
    def float_try_parse(num):
        try:
            if " " in num:
                raise ValueError()
            else:
                return True, float(num)
        except ValueError as ex:
            return False, num

    def __write_str(self, index, data):
        if len(data) < 15:
            self.__bp.set_data(index, data)

    def __set_str(self, index, c):
        """Description: Method validates control panel input and sets data to
        the selected blueprint field
        """
        dt = str(self.__bp.get_data().get(index))
        if dt is None:
            dt = ""
        dt += c
        parsing_calls = {
            BP.TYPES.get("ATTRIBUTE"): self.attribute_data_parsing,
            BP.TYPES.get("CHARACTER"): self.character_data_parsing,
            BP.TYPES.get("SPRITE"): self.sprite_data_parsing,
            BP.TYPES.get("FUNCTION"): self.function_data_parsing,
            BP.TYPES.get("SYSTEM"): self.system_data_parsing
        }
        try:
            parsing_calls[self.__bp.get_blueprint().get_type()](index, dt)
        except KeyError:
            pass

    def attribute_data_parsing(self, index, data):
        if index == 3:
            if self.__bp.get_blueprint().get_data_type() == AB.NONE:
                self.__write_str(index, StringUtils.get_string("ID_NONE"))
            elif self.__bp.get_blueprint().get_data_type() == AB.INT:
                if self.int_try_parse(data)[0]:
                    self.__write_str(index, data)
                else:
                    self.__write_str(index, data[:-1])
            elif self.__bp.get_blueprint().get_data_type() == AB.FLOAT:
                if self.float_try_parse(data)[0]:
                    self.__write_str(index, data)
                else:
                    self.__write_str(index, data[:-1])
            elif self.__bp.get_blueprint().get_data_type() == AB.STRING:
                self.__write_str(index, data)
            elif self.__bp.get_blueprint().get_data_type() == AB.CHAR:
                self.__write_str(index, data[-1])
        else:
            self.__write_str(index, data)

    def character_data_parsing(self, index, data):
        if 2 <= index <= 5:
            if self.int_try_parse(data)[0]:
                self.__write_str(index, data)
            else:
                self.__write_str(index, data[:-1])
        else:
            self.__write_str(index, data)

    def function_data_parsing(self, index, data):
        pass

    def sprite_data_parsing(self, index, data):
        pass

    def system_data_parsing(self, index, data):
        if index == 2 or index == 3 or 7 < index < 11:
            if self.int_try_parse(data)[0]:
                for c in data:
                    if c == "0":
                        data = data[1:]
                    else:
                        break
                if 7 < index < 11:
                    if len(data) < 4 and int(data) < 256:
                        self.__write_str(index, data)
                else:
                    self.__write_str(index, data)
            else:
                self.__write_str(index, data[:-1])
        else:
            self.__write_str(index, data)
