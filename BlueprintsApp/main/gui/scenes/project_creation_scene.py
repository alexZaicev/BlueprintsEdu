from gui.scenes.scene_builder import SceneBuilder
from utils import logger_utils, app_utils
from utils.string_utils import StringUtils
import pygame as pg
from pygame.locals import *
from utils.app_utils import Images
from gui.buttons.cancel_button import CancelButton
from gui.buttons.create_button import CreateButton
from utils.app_utils import GameApi


class ProjectCreationScene(SceneBuilder):

    def __init__(self, display, theme):
        SceneBuilder.__init__(self, display, theme)
        self.__logger = logger_utils.get_logger(__name__)
        self.input = None
        self.__project_name = ""
        self.api_select = None
        self.__api = " --- " + StringUtils.get_string("ID_SELECT") + " --- "
        self.btn_drop_down = None
        self.btn_create = CreateButton(self.theme, 0)
        self.btn_create.set_custom_coordinates(
            (app_utils.BOARD_WIDTH * .87, app_utils.BOARD_HEGHT * .8))
        self.btn_cancel = CancelButton(self.theme, 0)
        self.btn_cancel.set_custom_coordinates(
            (app_utils.BOARD_WIDTH * .87, app_utils.BOARD_HEGHT * .9))
        self.__is_drop_down_pressed = False
        self.__menu_content = []
        self.__menu_counter = 0

    def get_icon(self, menu):
        img = pg.image.load(Images.DROP_DOWN)
        img_rect = img.get_rect()
        img_rect.midright = (
            int(menu.right - app_utils.BOARD_WIDTH * .01), int(menu.center[1]))
        return (img, img_rect)

    def draw_scene(self):
        # PREPARE DATA
        font = pg.font.Font(self.theme.get("banner_font_style"),
                            int(app_utils.BOARD_WIDTH * .05))
        txt_title = font.render(StringUtils.get_string(
            "ID_TITLE") + ":", True, self.theme.get("font"))
        rect_title = txt_title.get_rect()
        rect_title.topleft = (int(app_utils.BOARD_WIDTH * .05),
                              int(app_utils.BOARD_HEGHT * .15))
        txt_api = font.render(StringUtils.get_string(
            "ID_GAME_API") + ":", True, self.theme.get("font"))
        rect_api = txt_api.get_rect()
        rect_api.topleft = (int(int(app_utils.BOARD_WIDTH * .05)),
                            int(rect_title.top + rect_title.height + app_utils.BOARD_HEGHT * .1))
        self.input = pg.Rect((int(rect_api.right + app_utils.BOARD_WIDTH * .05), int(rect_title.top)),
                             (int(app_utils.BOARD_WIDTH * 0.6), int(app_utils.BOARD_WIDTH * .05)))
        font = pg.font.Font(self.theme.get("text_font_style"),
                            int(app_utils.BOARD_WIDTH * .03))
        txt_input = font.render(self.__project_name,
                                True, self.theme.get("text_area_text"))
        rect_input = txt_input.get_rect()
        rect_input.center = self.input.center
        self.api_select = pg.Rect((int(rect_api.right + app_utils.BOARD_WIDTH * .05), int(rect_api.top)),
                                  (int(app_utils.BOARD_WIDTH * 0.6), int(app_utils.BOARD_WIDTH * .05)))
        txt_select = font.render(
            self.__api, True, self.theme.get("text_area_text"))
        rect_select = txt_select.get_rect()
        rect_select.center = self.api_select.center
        self.btn_drop_down = self.get_icon(self.api_select)
        # DISPLAY
        self.display.fill(self.theme.get("front_screen"))
        self.display.blit(txt_title, rect_title)
        self.display.blit(txt_api, rect_api)
        pg.draw.rect(self.display, self.theme.get(
            "text_area_background"), self.input, 0)
        self.display.blit(txt_input, rect_input)
        pg.draw.rect(self.display, self.theme.get(
            "text_area_background"), self.api_select, 0)
        self.display.blit(self.btn_drop_down[0], self.btn_drop_down[1])
        self.display.blit(txt_select, rect_select)
        self.draw_buttons()
        self.draw_drop_down(font)
        self.check_button_hover()
        super().draw_scene()

    def draw_drop_down(self, font):
        if self.__is_drop_down_pressed:
            self.__menu_content.clear()
            for pos in range(self.__menu_counter, len(GameApi.APIS), 1):
                if (pos - self.__menu_counter) < 3:
                    rect = pg.Rect((self.api_select.x, int(self.api_select.y + self.api_select.height * ((pos - self.__menu_counter) + 1))),
                                   (int(app_utils.BOARD_WIDTH * 0.6), int(app_utils.BOARD_WIDTH * .05)))
                    txt = font.render(GameApi.get_api(
                        pos)[1], True, self.theme.get("text_area_text"))
                    rect_txt = txt.get_rect()
                    rect_txt.center = rect.center
                    self.__menu_content.append(
                        [rect, txt, rect_txt]
                    )
            for i in range(0, len(self.__menu_content), 1):
                pg.draw.rect(self.display, self.theme.get(
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
        if event.type == MOUSEBUTTONUP:
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
                    self.__selected = True

    def check_button_pressed(self, event, board, pos):
        if self.btn_create.get_rect().collidepoint(pos) == 1:
            # TODO validate project details
            self.btn_create.on_click(board, (self.__project_name, self.__api))
        elif self.btn_cancel.get_rect().collidepoint(pos) == 1:
            self.btn_cancel.on_click(board)
        elif self.btn_drop_down[1].collidepoint(pos) == 1:
            if self.__is_drop_down_pressed:
                self.__is_drop_down_pressed = False
            else:
                self.__is_drop_down_pressed = True
                self.__menu_counter = 0

    def check_button_hover(self):
        # BUTTON HOVERING
        if self.btn_create.is_hovered(pg.mouse.get_pos()):
            self.btn_create.color = self.theme.get("selection_background")
        else:
            self.btn_create.color = self.theme.get("button")
        if self.btn_cancel.is_hovered(pg.mouse.get_pos()):
            self.btn_cancel.color = self.theme.get("selection_background")
        else:
            self.btn_cancel.color = self.theme.get("button")

    def check_key_pressed(self, event):
        if event.type == KEYDOWN:
            if event.key == K_a and len(self.__project_name) <= 33:
                self.__project_name += "a"
            elif event.key == K_b and len(self.__project_name) <= 33:
                self.__project_name += "b"
            elif event.key == K_c and len(self.__project_name) <= 33:
                self.__project_name += "c"
            elif event.key == K_d and len(self.__project_name) <= 33:
                self.__project_name += "d"
            elif event.key == K_e and len(self.__project_name) <= 33:
                self.__project_name += "e"
            elif event.key == K_f and len(self.__project_name) <= 33:
                self.__project_name += "f"
            elif event.key == K_g and len(self.__project_name) <= 33:
                self.__project_name += "g"
            elif event.key == K_h and len(self.__project_name) <= 33:
                self.__project_name += "h"
            elif event.key == K_i and len(self.__project_name) <= 33:
                self.__project_name += "i"
            elif event.key == K_j and len(self.__project_name) <= 33:
                self.__project_name += "j"
            elif event.key == K_k and len(self.__project_name) <= 33:
                self.__project_name += "k"
            elif event.key == K_l and len(self.__project_name) <= 33:
                self.__project_name += "l"
            elif event.key == K_m and len(self.__project_name) <= 33:
                self.__project_name += "m"
            elif event.key == K_n and len(self.__project_name) <= 33:
                self.__project_name += "n"
            elif event.key == K_o and len(self.__project_name) <= 33:
                self.__project_name += "o"
            elif event.key == K_p and len(self.__project_name) <= 33:
                self.__project_name += "p"
            elif event.key == K_q and len(self.__project_name) <= 33:
                self.__project_name += "q"
            elif event.key == K_r and len(self.__project_name) <= 33:
                self.__project_name += "r"
            elif event.key == K_s and len(self.__project_name) <= 33:
                self.__project_name += "s"
            elif event.key == K_t and len(self.__project_name) <= 33:
                self.__project_name += "t"
            elif event.key == K_u and len(self.__project_name) <= 33:
                self.__project_name += "u"
            elif event.key == K_v and len(self.__project_name) <= 33:
                self.__project_name += "v"
            elif event.key == K_w and len(self.__project_name) <= 33:
                self.__project_name += "w"
            elif event.key == K_x and len(self.__project_name) <= 33:
                self.__project_name += "x"
            elif event.key == K_y and len(self.__project_name) <= 33:
                self.__project_name += "y"
            elif event.key == K_z and len(self.__project_name) <= 33:
                self.__project_name += "z"
            elif (event.key == K_0 or event.key == K_KP0) and len(self.__project_name) <= 33:
                self.__project_name += "0"
            elif (event.key == K_1 or event.key == K_KP1) and len(self.__project_name) <= 33:
                self.__project_name += "1"
            elif (event.key == K_2 or event.key == K_KP2) and len(self.__project_name) <= 33:
                self.__project_name += "2"
            elif (event.key == K_3 or event.key == K_KP3) and len(self.__project_name) <= 33:
                self.__project_name += "3"
            elif (event.key == K_4 or event.key == K_KP4) and len(self.__project_name) <= 33:
                self.__project_name += "4"
            elif (event.key == K_5 or event.key == K_KP5) and len(self.__project_name) <= 33:
                self.__project_name += "5"
            elif (event.key == K_6 or event.key == K_KP6) and len(self.__project_name) <= 33:
                self.__project_name += "6"
            elif (event.key == K_7 or event.key == K_KP7) and len(self.__project_name) <= 33:
                self.__project_name += "7"
            elif (event.key == K_8 or event.key == K_KP8) and len(self.__project_name) <= 33:
                self.__project_name += "8"
            elif (event.key == K_9 or event.key == K_KP9) and len(self.__project_name) <= 33:
                self.__project_name += "9"
            elif event.key == K_DELETE or event.key == K_BACKSPACE:
                if len(self.__project_name) != 0:
                    self.__project_name = self.__project_name[:-1]
