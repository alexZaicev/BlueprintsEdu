from gui.scenes.scene_builder import SceneBuilder
from utils import logger_utils
from utils.gui_utils import Themes
import pygame as pg
from utils import app_utils, gui_utils
from utils.string_utils import StringUtils
from gui.forms.control_panel_form import ControlPanelForm
from gui.forms.blueprint_control_form import BlueprintControlForm
from gui.buttons.exit_button import ExitButton
from pygame.locals import *
from gui.buttons.develop_menu_buttons import *


class DevelopmentScene(SceneBuilder):

    BTN_SIZE = [1.1, .05]

    def __init__(self, display, project):
        SceneBuilder.__init__(self, display)
        self.__project = (project.get("PROJECT_NAME"), project.get("PROJECT_API"))
        pg.display.set_caption("{} - {}   {}".format(self.__project[0], self.__project[1], app_utils.CAPTION))

        self.__logger = logger_utils.get_logger(__name__)
        self.__logger.debug("{} --- {}".format(self.__project[0], self.__project[1]))

        self.btn_file = FileButton()
        self.btn_file.color = Themes.DEFAULT_THEME.get("background")
        self.btn_run = RunButton()
        self.btn_run.color = Themes.DEFAULT_THEME.get("background")
        self.btn_settings = SettingsButton()
        self.btn_settings.color = Themes.DEFAULT_THEME.get("background")
        self.btn_edit = EditButton()
        self.btn_edit.color = Themes.DEFAULT_THEME.get("background")
        self.__init_btn_size()
        self.__file_menu_content = self.__init_file_menu()
        self.__edit_menu_content = self.__init_edit_menu()
        self.__btn_file_pressed, self.__btn_edit_pressed, self.__btn_run_pressed, \
            self.__btn_settings_pressed = False, False, False, False

        self.__cont_panel = ControlPanelForm(self.display,
                                             (int(app_utils.BOARD_WIDTH * .005), int(self.btn_file.get_rect().bottom * 1.005)),
                                             (int(app_utils.BOARD_WIDTH * .265), int(app_utils.BOARD_HEGHT * .945)))
        self.__bp_panel = BlueprintControlForm(self.__cont_panel, self.display, self.__project,
                                               (int(self.__cont_panel.get_rect().right + app_utils.BOARD_WIDTH * .005),
                                                int(self.btn_file.get_rect().bottom * 1.05)),
                                               (int(app_utils.BOARD_WIDTH * .723),
                                                int(app_utils.BOARD_HEGHT * .945)))
        if project.get("CONNECTIONS") is not None and project.get("BLUEPRINTS") is not None:
            self.__bp_panel.load_project(project.get("CONNECTIONS"), project.get("BLUEPRINTS"))

# ----------------INITIALIZATIONS----------------

    def __init_btn_coords(self):
        self.btn_file.set_custom_coordinates(
            (int(app_utils.BOARD_WIDTH * gui_utils.BUTTON_MENU_MARGIN + self.btn_file.get_rect().width * .5),
             int(0 + self.btn_file.get_rect().height * .5)))
        self.btn_edit.set_custom_coordinates(
            (int(self.btn_file.get_rect().right + (self.btn_run.get_rect().width * .5
                                                   + app_utils.BOARD_WIDTH * gui_utils.BUTTON_MENU_MARGIN)), int(0 + self.btn_file.get_rect().height * .5)))
        self.btn_run.set_custom_coordinates(
            (int(self.btn_edit.get_rect().right + (self.btn_run.get_rect().width * .5
                                                   + app_utils.BOARD_WIDTH * gui_utils.BUTTON_MENU_MARGIN)),
             int(0 + self.btn_run.get_rect().height * .5)))
        self.btn_settings.set_custom_coordinates((
            int(self.btn_run.get_rect().right + (self.btn_settings.get_rect().width * .5
                                                 + app_utils.BOARD_WIDTH * gui_utils.BUTTON_MENU_MARGIN)),
            int(0 + self.btn_settings.get_rect().height * .5)))

    def __init_btn_size(self):
        self.btn_file.set_custom_size(DevelopmentScene.BTN_SIZE)
        self.btn_edit.set_custom_size(DevelopmentScene.BTN_SIZE)
        self.btn_run.set_custom_size(DevelopmentScene.BTN_SIZE)
        self.btn_settings.set_custom_size(DevelopmentScene.BTN_SIZE)
        self.__init_btn_coords()

    def __init_file_menu(self):
        result = []
        r = self.btn_file.get_rect()
        # TODO investigate why r.left offset is different for each button

        save = SaveButton()
        save.set_custom_size(DevelopmentScene.BTN_SIZE)
        save.set_topleft((int(r.left + app_utils.BOARD_WIDTH * .003), r.bottom))
        save.color = Themes.DEFAULT_THEME.get("menu_background")

        sae = SaveExitButton()
        sae.set_custom_size(DevelopmentScene.BTN_SIZE)
        sae.set_topleft((int(r.left + app_utils.BOARD_WIDTH * .001), save.get_rect().bottom))
        sae.color = Themes.DEFAULT_THEME.get("menu_background")

        exit = ExitButton()
        exit.set_custom_size(DevelopmentScene.BTN_SIZE)
        exit.set_topleft((int(r.left + app_utils.BOARD_WIDTH * .005), sae.get_rect().bottom))
        exit.color = Themes.DEFAULT_THEME.get("menu_background")

        result.extend([save, sae, exit])
        return result

    def __init_edit_menu(self):
        result = []
        r = self.btn_edit.get_rect()
        add_attr = AddAttrButton()
        add_attr.set_custom_size(DevelopmentScene.BTN_SIZE)
        add_attr.set_topleft((int(r.left + app_utils.BOARD_WIDTH * .002), r.bottom))
        add_attr.color = Themes.DEFAULT_THEME.get("menu_background")

        add_char = AddCharacterButton()
        add_char.set_custom_size(DevelopmentScene.BTN_SIZE)
        add_char.set_topleft((int(r.left + app_utils.BOARD_WIDTH * .002), add_attr.get_rect().bottom))
        add_char.color = Themes.DEFAULT_THEME.get("menu_background")

        add_func = AddFunctionButton()
        add_func.set_custom_size(DevelopmentScene.BTN_SIZE)
        add_func.set_topleft((int(r.left + app_utils.BOARD_WIDTH * .002), add_char.get_rect().bottom))
        add_func.color = Themes.DEFAULT_THEME.get("menu_background")

        add_sprite = AddSpriteButton()
        add_sprite.set_custom_size(DevelopmentScene.BTN_SIZE)
        add_sprite.set_topleft((int(r.left + app_utils.BOARD_WIDTH * .002), add_func.get_rect().bottom))
        add_sprite.color = Themes.DEFAULT_THEME.get("menu_background")

        result.extend([add_attr, add_char, add_func, add_sprite])
        return result

# ----------------END----------------

    def draw_menu_buttons(self):
        """Description: function draws development menu navigation barself.
            Button <<FILE>>: Opens project/file manipulation to the user
            Button <<RUN>>: Opens run/build project manipulation to the user
            Button <<SETTINGS>>: Opens blueprints/blueprint development window manipulation to the user
        """
        self.check_button_hover()
        pg.draw.rect(self.display, self.btn_settings.color, self.btn_settings.get_rect(), 0)
        self.display.blit(self.btn_settings.get_text(), self.btn_settings.get_text_rect())
        pg.draw.rect(self.display, self.btn_run.color, self.btn_run.get_rect(), 0)
        self.display.blit(self.btn_run.get_text(), self.btn_run.get_text_rect())
        pg.draw.rect(self.display, self.btn_file.color, self.btn_file.get_rect(), 0)
        self.display.blit(self.btn_file.get_text(), self.btn_file.get_text_rect())
        pg.draw.rect(self.display, self.btn_edit.color, self.btn_edit.get_rect(), 0)
        self.display.blit(self.btn_edit.get_text(), self.btn_edit.get_text_rect())

    def draw_drop_down(self):
        def __draw_file_menu():
            r = pg.Rect((self.btn_file.get_rect().left, self.btn_file.get_rect().bottom),
                        (int(app_utils.BOARD_WIDTH * .15), int(self.btn_file.get_rect().height * len(self.__file_menu_content))))
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("menu_background"), r, 0)
            for btn in self.__file_menu_content:
                pg.draw.rect(self.display, btn.color, btn.get_rect(), 0)
                self.display.blit(btn.get_text(), btn.get_text_rect())

        def __draw_edit_menu():
            r = pg.Rect((self.btn_edit.get_rect().left, self.btn_edit.get_rect().bottom),
                        (int(app_utils.BOARD_WIDTH * .15), int(self.btn_file.get_rect().height * len(self.__edit_menu_content))))
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("menu_background"), r, 0)
            for btn in self.__edit_menu_content:
                pg.draw.rect(self.display, btn.color, btn.get_rect(), 0)
                self.display.blit(btn.get_text(), btn.get_text_rect())

        def __draw_run_menu():
            pass

        def __draw_settings_menu():
            pass

        if self.__btn_file_pressed:
            __draw_file_menu()
        elif self.__btn_edit_pressed:
            __draw_edit_menu()
        elif self.__btn_run_pressed:
            pass
        elif self.__btn_settings_pressed:
            pass

    def draw_scene(self):
        """Description: main scene drawing function, orchestrating component drawings on display
        """
        self.display.fill(Themes.DEFAULT_THEME.get("background"))
        self.draw_menu_buttons()
        self.__cont_panel.draw_form()
        self.__bp_panel.draw_form()
        self.draw_drop_down()
        super().draw_scene()

    def check_button_hover(self):
        if not self.__btn_settings_pressed:
            if self.btn_settings.is_hovered(pg.mouse.get_pos()):
                self.btn_settings.color = Themes.DEFAULT_THEME.get("selection_background")
            else:
                self.btn_settings.color = Themes.DEFAULT_THEME.get("background")
        else:
            self.btn_settings.color = Themes.DEFAULT_THEME.get("selection_background")
        if not self.__btn_run_pressed:
            if self.btn_run.is_hovered(pg.mouse.get_pos()):
                self.btn_run.color = Themes.DEFAULT_THEME.get("selection_background")
            else:
                self.btn_run.color = Themes.DEFAULT_THEME.get("background")
        else:
            self.btn_run.color = Themes.DEFAULT_THEME.get("selection_background")
        if not self.__btn_file_pressed:
            if self.btn_file.is_hovered(pg.mouse.get_pos()):
                self.btn_file.color = Themes.DEFAULT_THEME.get("selection_background")
            else:
                self.btn_file.color = Themes.DEFAULT_THEME.get("background")
        else:
            self.btn_file.color = Themes.DEFAULT_THEME.get("selection_background")
        if not self.__btn_edit_pressed:
            if self.btn_edit.is_hovered(pg.mouse.get_pos()):
                self.btn_edit.color = Themes.DEFAULT_THEME.get("selection_background")
            else:
                self.btn_edit.color = Themes.DEFAULT_THEME.get("background")
        else:
            self.btn_edit.color = Themes.DEFAULT_THEME.get("selection_background")

    def check_events(self, event, board):
        super().check_events(event, board)

        def __reset_btn_menu():
            self.__btn_file_pressed = False
            self.__btn_edit_pressed = False
            self.__btn_run_pressed = False
            self.__btn_settings_pressed = False

        def __check_file_menu_press(pos, board):
            if self.__btn_file_pressed:
                for btn in self.__file_menu_content:
                    if btn.get_rect().collidepoint(pos):
                        if isinstance(btn, SaveButton) or isinstance(btn, SaveExitButton):
                            btn.on_click(board, self.__bp_panel)
                        else:
                            btn.on_click(board)

        def __check_edit_menu_press(pos, board):
            if self.__btn_edit_pressed:
                for btn in self.__edit_menu_content:
                    if btn.get_rect().collidepoint(pos):
                        btn.on_click(board, self.__bp_panel)

        if event.type == MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            if self.btn_file.get_rect().collidepoint(pos):
                if self.__btn_file_pressed:
                    __reset_btn_menu()
                else:
                    __reset_btn_menu()
                    self.__btn_file_pressed = True
            elif self.btn_edit.get_rect().collidepoint(pos):
                if self.__btn_edit_pressed:
                    __reset_btn_menu()
                else:
                    __reset_btn_menu()
                    self.__btn_edit_pressed = True
            else:
                __check_file_menu_press(pos, board)
                __check_edit_menu_press(pos, board)
                __reset_btn_menu()
        self.__cont_panel.check_form_events(event)
        self.__bp_panel.check_form_events(event)
