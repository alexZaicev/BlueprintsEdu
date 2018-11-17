import pygame as pg
from pygame.locals import *

from gui.buttons.cancel_button import CancelButton
from gui.buttons.create_button import CreateButton
from gui.popup import Popup
from gui.scenes.scene_builder import SceneBuilder
from utils import logger_utils
from utils.app_utils import DisplaySettings
from utils.app_utils import GameApi
from utils.app_utils import Images, Events
from utils.gui_utils import Themes
from utils.string_utils import StringUtils


class ProjectCreationScene(SceneBuilder):

    def __init__(self, display):
        SceneBuilder.__init__(self, display)
        self.__logger = logger_utils.get_logger(__name__)
        self.input = None
        self.__project_name = ""
        self.api_select = None
        self.__api = GameApi.DEFAULT_API
        self.btn_drop_down = None
        self.btn_create = CreateButton(1)
        self.btn_cancel = CancelButton(0)
        self.__is_drop_down_pressed = False
        self.__menu_content = []
        self.__menu_counter = 0
        self.__popup = None

    def draw_scene(self):
        # PREPARE DATA
        if self.__api == GameApi.DEFAULT_API:
            self.__api = " --- {} ---".format(StringUtils.get_string("ID_SELECT"))

        font = pg.font.Font(Themes.DEFAULT_THEME.get("banner_font_style"),
                            int(DisplaySettings.get_size_by_key()[0] * .05))
        txt_title = font.render(StringUtils.get_string(
            "ID_TITLE") + ":", True, Themes.DEFAULT_THEME.get("font"))
        rect_title = txt_title.get_rect()
        rect_title.topleft = (int(DisplaySettings.get_size_by_key()[0] * .05),
                              int(DisplaySettings.get_size_by_key()[1] * .15))
        txt_api = font.render(StringUtils.get_string(
            "ID_GAME_API") + ":", True, Themes.DEFAULT_THEME.get("font"))
        rect_api = txt_api.get_rect()
        rect_api.topleft = (int(int(DisplaySettings.get_size_by_key()[0] * .05)),
                            int(rect_title.top + rect_title.height + DisplaySettings.get_size_by_key()[1] * .1))
        self.input = pg.Rect((int(rect_api.right + DisplaySettings.get_size_by_key()[0] * .05), int(rect_title.top)),
                             (int(DisplaySettings.get_size_by_key()[0] * 0.6),
                              int(DisplaySettings.get_size_by_key()[0] * .05)))
        font = pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"),
                            int(DisplaySettings.get_size_by_key()[0] * .03))
        txt_input = font.render(self.__project_name,
                                True, Themes.DEFAULT_THEME.get("text_area_text"))
        rect_input = txt_input.get_rect()
        rect_input.center = self.input.center
        self.api_select = pg.Rect((int(rect_api.right + DisplaySettings.get_size_by_key()[0] * .05), int(rect_api.top)),
                                  (int(DisplaySettings.get_size_by_key()[0] * 0.6),
                                   int(DisplaySettings.get_size_by_key()[0] * .05)))
        txt_select = font.render(
            self.__api, True, Themes.DEFAULT_THEME.get("text_area_text"))
        rect_select = txt_select.get_rect()
        rect_select.center = self.api_select.center
        # self.btn_drop_down = self.get_icon(self.api_select)
        img = Images.get_icon(Images.DROP_DOWN)
        img[1].midright = (int(self.api_select.right - DisplaySettings.get_size_by_key()[0] * .01),
                           int(self.api_select.center[1]))
        self.btn_drop_down = img
        # DISPLAY
        self.display.fill(Themes.DEFAULT_THEME.get("front_screen"))
        self.display.blit(txt_title, rect_title)
        self.display.blit(txt_api, rect_api)
        pg.draw.rect(self.display, Themes.DEFAULT_THEME.get(
            "text_area_background"), self.input, 0)
        self.display.blit(txt_input, rect_input)
        pg.draw.rect(self.display, Themes.DEFAULT_THEME.get(
            "text_area_background"), self.api_select, 0)
        self.display.blit(self.btn_drop_down[0], self.btn_drop_down[1])
        self.display.blit(txt_select, rect_select)
        self.draw_buttons()
        self.draw_drop_down(font)
        self.check_button_hover()
        if self.__popup is not None:
            self.__popup.draw(self.display)
        super().draw_scene()

    def draw_drop_down(self, font):
        if self.__is_drop_down_pressed:
            self.__menu_content.clear()
            for pos in range(self.__menu_counter, len(GameApi.APIS), 1):
                if (pos - self.__menu_counter) < 3:
                    rect = pg.Rect((self.api_select.x, int(
                        self.api_select.y + self.api_select.height * ((pos - self.__menu_counter) + 1))),
                                   (int(DisplaySettings.get_size_by_key()[0] * 0.6),
                                    int(DisplaySettings.get_size_by_key()[0] * .05)))
                    txt = font.render(GameApi.get_api(
                        pos)[1], True, Themes.DEFAULT_THEME.get("text_area_text"))
                    rect_txt = txt.get_rect()
                    rect_txt.center = rect.center
                    self.__menu_content.append(
                        [rect, txt, rect_txt]
                    )
            for i in range(0, len(self.__menu_content), 1):
                pg.draw.rect(self.display, Themes.DEFAULT_THEME.get(
                    "text_area_background"), self.__menu_content[i][0], 0)
                self.display.blit(
                    self.__menu_content[i][1], self.__menu_content[i][2])

    def draw_buttons(self):
        pg.draw.rect(self.display, self.btn_create.color,
                     self.btn_create.get_rect(), 0)
        self.display.blit(self.btn_create.get_text(),
                          self.btn_create.get_text_rect())
        pg.draw.rect(self.display, self.btn_cancel.color,
                     self.btn_cancel.get_rect(), 0)
        self.display.blit(self.btn_cancel.get_text(),
                          self.btn_cancel.get_text_rect())

    def check_events(self, event, board):
        super().check_events(event, board)
        self.check_key_pressed(event)
        if (event.type == MOUSEBUTTONDOWN) or (event.type == KEYDOWN):
            self.__popup = None
        elif event.type == MOUSEBUTTONUP:
            if event.button != 4 and event.button != 5:
                self.check_button_pressed(event, board, pg.mouse.get_pos())
                self.check_menu_pressed(pg.mouse.get_pos())
        elif event.type == MOUSEBUTTONDOWN:
            if self.__is_drop_down_pressed:
                if event.button == 4:
                    self.__menu_counter -= 1
                elif event.button == 5 and len(GameApi.APIS) > 3:
                    self.__menu_counter += 1
                if self.__menu_counter < 0:
                    self.__menu_counter = 0
                elif (len(GameApi.APIS) > 3) and (self.__menu_counter > len(GameApi.APIS) - 3):
                    self.__menu_counter = (len(GameApi.APIS) - 3)

    def check_menu_pressed(self, pos):
        if self.__is_drop_down_pressed:
            for i in range(0, len(self.__menu_content), 1):
                if self.__menu_content[i][0].collidepoint(pos) == 1:
                    self.__api = GameApi.APIS[i + self.__menu_counter][1]
                    self.__is_drop_down_pressed = False

    def check_button_pressed(self, event, board, pos):
        if self.btn_create.get_rect().collidepoint(pos) == 1 and self.validate_project_info():
            try:
                self.btn_create.on_click(board, {
                    "PROJECT_NAME": self.__project_name,
                    "PROJECT_API": self.__api
                })
            except FileExistsError as ex:
                self.__popup = Popup(Popup.POP_STATES.get("ERROR"), str(ex))
        elif self.btn_cancel.get_rect().collidepoint(pos) == 1:
            self.btn_cancel.on_click(board)
        elif self.btn_drop_down[1].collidepoint(pos) == 1:
            if self.__is_drop_down_pressed:
                self.__is_drop_down_pressed = False
            else:
                self.__is_drop_down_pressed = True
                self.__menu_counter = 0

    def validate_project_info(self):
        valid = True
        if (StringUtils.get_string("ID_SELECT") in self.__api) and (len(self.__project_name) < 5):
            valid = False
            self.__popup = Popup(Popup.POP_STATES.get("ERROR"), "Incorrect project details")
        elif StringUtils.get_string("ID_SELECT") in self.__api:
            valid = False
            self.__popup = Popup(Popup.POP_STATES.get("ERROR"), "API must be selected")
        elif len(self.__project_name) < 5:
            valid = False
            self.__popup = Popup(Popup.POP_STATES.get("ERROR"), "Project name should be greater than 5 chars")
        return valid

    def check_button_hover(self):
        # BUTTON HOVERING
        if self.btn_create.is_hovered(pg.mouse.get_pos()):
            self.btn_create.color = Themes.DEFAULT_THEME.get("selection_background")
        else:
            self.btn_create.color = Themes.DEFAULT_THEME.get("front_screen")
        if self.btn_cancel.is_hovered(pg.mouse.get_pos()):
            self.btn_cancel.color = Themes.DEFAULT_THEME.get("selection_background")
        else:
            self.btn_cancel.color = Themes.DEFAULT_THEME.get("front_screen")

    def check_key_pressed(self, event):
        if event.type == KEYDOWN or event.type == KEYUP:
            c = Events.get_char(event.key, event.type)
            if event.type == KEYDOWN:
                if c == Events.SPECIAL_KEYS.get("BACKSPACE"):
                    if len(self.__project_name) != 0:
                        self.__project_name = self.__project_name[:-1]
                elif c == Events.SPECIAL_KEYS.get("DELETE"):
                    self.__project_name = ""
                elif c == Events.SPECIAL_KEYS.get("UNREGISTERED"):
                    pass
                elif isinstance(c, str):
                    if len(self.__project_name) <= 25:
                        self.__project_name += c
