import pygame as pg
from pygame.locals import *

from gui.buttons.back_button import BackButton
from gui.buttons.delete_button import DeleteButton
from gui.buttons.select_button import SelectButton
from gui.scenes.scene_builder import SceneBuilder
from utils import logger_utils
from utils import scene_utils
from utils.app_utils import DisplaySettings
from utils.gui_utils import Themes
from utils.managers.project_manager import ProjectManager
from utils.string_utils import StringUtils


class LoadScene(SceneBuilder):

    def __init__(self, display):
        SceneBuilder.__init__(self, display)
        self.__logger = logger_utils.get_logger(__name__)
        self.btn_select = SelectButton(0)
        self.btn_select.color = Themes.DEFAULT_THEME.get("front_screen")
        self.btn_delete = DeleteButton(0)
        self.btn_delete.color = Themes.DEFAULT_THEME.get("front_screen")
        self.btn_back = BackButton(0)
        self.btn_back.color = Themes.DEFAULT_THEME.get("front_screen")
        self.file_container = pg.Rect(
            (int(DisplaySettings.get_size_by_key()[0] * .01), int(DisplaySettings.get_size_by_key()[1] * 0.22)),
            (int(DisplaySettings.get_size_by_key()[0] * .98), int(DisplaySettings.get_size_by_key()[1] * .66)))
        self.files = ProjectManager.get_projects()
        self.__logger.debug(self.files)

    def draw_scene(self):
        # PREPARE DATA FOR DISPLAY
        font = pg.font.Font(Themes.DEFAULT_THEME.get("banner_font_style"),
                            int(DisplaySettings.get_size_by_key()[1] * 0.09))
        header = font.render(StringUtils.get_string(
            "ID_SAVED_PROJECTS"), True, Themes.DEFAULT_THEME.get("font"))
        header_rect = header.get_rect()
        header_rect.topleft = (
            int(DisplaySettings.get_size_by_key()[0] * .02), int(DisplaySettings.get_size_by_key()[1] * .05))
        # PUSH TO DISPLAY
        self.display.fill(Themes.DEFAULT_THEME.get("front_screen"))
        self.display.blit(header, header_rect)
        self.draw_container(header_rect)
        self.draw_buttons()
        self.check_button_hover()
        self.draw_selected_file_boarder()
        super().draw_scene()

    def draw_container(self, header_rect):
        pg.draw.rect(self.display, Themes.DEFAULT_THEME.get(
            "panel_background"), self.file_container, 0)
        # DISPLAY PROJECT FILES
        for pos in range(0, len(self.files), 1):
            text = self.files[pos].get_texts(self.file_container, pos)
            if pos % 2 == 0:
                # color light
                self.files[pos].set_rect(self.file_container, pos)
                pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("panel_front_light"),
                             self.files[pos].get_rect(), 0)
                self.display.blit(text[0][0], text[0][1])
                self.display.blit(text[1][0], text[1][1])
            else:
                # color dark
                self.files[pos].set_rect(self.file_container, pos)
                pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("panel_front_dark"),
                             self.files[pos].get_rect(), 0)
                self.display.blit(text[0][0], text[0][1])
                self.display.blit(text[1][0], text[1][1])

    def draw_buttons(self):
        self.btn_select.set_custom_coordinates((
            int((DisplaySettings.get_size_by_key()[0] - self.btn_select.get_rect().width * .5) * .98),
            int(self.file_container.bottom + DisplaySettings.get_size_by_key()[
                1] * 0.015 + self.btn_select.get_rect().height * .5)))
        self.btn_delete.set_custom_coordinates((
            int(self.btn_select.get_rect().left - (
                    DisplaySettings.get_size_by_key()[0] * .005 + self.btn_delete.get_rect().width * .5)),
            int(self.file_container.bottom + DisplaySettings.get_size_by_key()[
                1] * 0.015 + self.btn_delete.get_rect().height * .5)))
        self.btn_back.set_custom_coordinates((
            int(self.btn_delete.get_rect().left - (
                    DisplaySettings.get_size_by_key()[0] * .005 + self.btn_back.get_rect().width * .5)),
            int(self.file_container.bottom + DisplaySettings.get_size_by_key()[
                1] * 0.015 + self.btn_back.get_rect().height * .5)))
        pg.draw.rect(self.display, self.btn_select.color,
                     self.btn_select.get_rect(), 0)
        self.display.blit(self.btn_select.get_text(),
                          self.btn_select.get_text_rect())
        pg.draw.rect(self.display, self.btn_delete.color,
                     self.btn_delete.get_rect(), 0)
        self.display.blit(self.btn_delete.get_text(),
                          self.btn_delete.get_text_rect())
        pg.draw.rect(self.display, self.btn_back.color,
                     self.btn_back.get_rect(), 0)
        self.display.blit(self.btn_back.get_text(),
                          self.btn_back.get_text_rect())

    def draw_selected_file_boarder(self):
        for f in self.files:
            if f.pressed:
                pg.draw.rect(self.display, Themes.DEFAULT_THEME.get(
                    "selection_background"), f.get_rect(), 3)

    def check_button_press(self, pos, board):
        if self.btn_select.get_rect().collidepoint(pos) == 1:
            self.__logger.debug("Select pressed")
            for f in self.files:
                if f.pressed:
                    self.btn_select.on_click(board, f.get_name())
        elif self.btn_delete.get_rect().collidepoint(pos) == 1:
            self.__logger.debug("Delete pressed")
            for f in self.files:
                if f.pressed:
                    self.btn_delete.on_click(board, f.get_name())
                    self.update_file_container(board)
        elif self.btn_back.get_rect().collidepoint(pos) == 1:
            self.btn_back.on_click(board)

    def update_file_container(self, board):
        try:
            self.files = ProjectManager.get_projects()
        except FileNotFoundError:
            board.set_scene(scene_utils.WELCOME_SCENE)

    def check_file_press(self, pos):
        for f in self.files:
            f.pressed = False
            if f.get_rect() is not None and f.get_rect().collidepoint(pos) == 1:
                f.pressed = True

    def check_events(self, event, board):
        super().check_events(event, board)
        if event.type == MOUSEBUTTONDOWN:
            self.check_button_press(pg.mouse.get_pos(), board)
            self.check_file_press(pg.mouse.get_pos())

    def check_button_hover(self):
        # BUTTON HOVERING
        if self.btn_select.is_hovered(pg.mouse.get_pos()):
            self.btn_select.color = Themes.DEFAULT_THEME.get("selection_background")
        else:
            self.btn_select.color = Themes.DEFAULT_THEME.get("front_screen")
        if self.btn_delete.is_hovered(pg.mouse.get_pos()):
            self.btn_delete.color = Themes.DEFAULT_THEME.get("selection_background")
        else:
            self.btn_delete.color = Themes.DEFAULT_THEME.get("front_screen")
        if self.btn_back.is_hovered(pg.mouse.get_pos()):
            self.btn_back.color = Themes.DEFAULT_THEME.get("selection_background")
        else:
            self.btn_back.color = Themes.DEFAULT_THEME.get("front_screen")
