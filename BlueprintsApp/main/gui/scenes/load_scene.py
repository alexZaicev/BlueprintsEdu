from gui.scenes.scene_builder import SceneBuilder
import pygame as pg
from utils.app_utils import Images
from utils import app_utils, logger_utils
from pygame.locals import *
from utils import scene_utils, gui_utils
from gui.buttons.select_button import SelectButton
from gui.buttons.delete_button import DeleteButton
from utils.string_utils import StringUtils
from project_manager import ProjectManager


class LoadScene(SceneBuilder):

    def __init__(self, display, theme):
        SceneBuilder.__init__(self, display, theme)
        self.__logger = logger_utils.get_logger(__name__)
        self.icons = self.get_icons()
        self.btn_select = SelectButton(theme, 0)
        self.btn_delete = DeleteButton(theme, 0)
        self.file_container = pg.Rect((int(app_utils.BOARD_WIDTH * .01), int(app_utils.BOARD_HEGHT * 0.22)),
                                      (int(app_utils.BOARD_WIDTH * .98), int(app_utils.BOARD_HEGHT * .66)))
        self.files = ProjectManager.get_projects(self.theme)
        self.__logger.debug(self.files)

    def get_icons(self):
        result = []
        img = pg.image.load(Images.UNDO)
        img_rect = img.get_rect()
        img_rect.topleft = (int(app_utils.BOARD_WIDTH * .01),
                            int(app_utils.BOARD_HEGHT * 0.02))
        result.append([img, img_rect])
        return result

    def draw_scene(self):
        # PREPARE DATA FOR DISPLAY
        font = pg.font.Font(self.theme.get("banner_font_style"),
                            int(app_utils.BOARD_HEGHT * 0.09))
        header = font.render(StringUtils.get_string(
            "ID_SAVED_PROJECTS"), True, self.theme.get("font"))
        header_rect = header.get_rect()
        header_rect.topleft = (
            int(app_utils.BOARD_WIDTH * .05), int(app_utils.BOARD_HEGHT * 0.1))
        # PUSH TO DISPLAY
        self.display.fill(self.theme.get("front_screen"))
        for i in self.icons:
            self.display.blit(i[0], i[1])
        self.display.blit(header, header_rect)
        self.draw_container(header_rect)
        self.draw_buttons()
        self.check_button_hover()
        self.draw_selected_file_boarder()
        super().draw_scene()

    def draw_container(self, header_rect):
        self.btn_select.set_custom_coordinates((
            int((app_utils.BOARD_WIDTH - self.btn_select.get_rect().width * .5) * .98),
            int(self.file_container.bottom + app_utils.BOARD_HEGHT * 0.015 + self.btn_select.get_rect().height * .5)))
        self.btn_delete.set_custom_coordinates((
            int((app_utils.BOARD_WIDTH - self.btn_delete.get_rect().width * 1.5) * .965),
            int(self.file_container.bottom + app_utils.BOARD_HEGHT * 0.015 + self.btn_delete.get_rect().height * .5)))
        pg.draw.rect(self.display, self.theme.get(
            "panel_background"), self.file_container, 0)
        # DISPLAY PROJECT FILES
        for pos in range(0, len(self.files), 1):
            text = self.files[pos].get_texts(self.file_container, pos)
            if pos % 2 == 0:
                # color light
                self.files[pos].set_rect(self.file_container, pos)
                pg.draw.rect(self.display, self.theme.get("panel_front_light"),
                             self.files[pos].get_rect(), 0)
                self.display.blit(text[0][0], text[0][1])
                self.display.blit(text[1][0], text[1][1])
            else:
                # color dark
                self.files[pos].set_rect(self.file_container, pos)
                pg.draw.rect(self.display, self.theme.get("panel_front_dark"),
                             self.files[pos].get_rect(), 0)
                self.display.blit(text[0][0], text[0][1])
                self.display.blit(text[1][0], text[1][1])

    def draw_buttons(self):
        pg.draw.rect(self.display, self.btn_select.color,
                     self.btn_select.get_rect(), 0)
        self.display.blit(self.btn_select.get_text(),
                          self.btn_select.get_text_rect())
        pg.draw.rect(self.display, self.btn_delete.color,
                     self.btn_delete.get_rect(), 0)
        self.display.blit(self.btn_delete.get_text(),
                          self.btn_delete.get_text_rect())

    def draw_selected_file_boarder(self):
        for f in self.files:
            if f.pressed:
                pg.draw.rect(self.display, self.theme.get(
                    "selection_background"), f.get_rect(), 10)

    def check_button_press(self, pos, board):
        if self.icons[0][1].collidepoint(pos) == 1:
            board.set_scene(scene_utils.WELCOME_SCENE)
        elif self.btn_select.get_rect().collidepoint(pos) == 1:
            self.__logger.debug("Select pressed")
            for f in self.files:
                if f.pressed:
                    self.btn_select.on_click(board, f.get_name())
        elif self.btn_delete.get_rect().collidepoint(pos) == 1:
            self.__logger.debug("Delete pressed")
            for f in self.files:
                if f.pressed:
                    self.btn_delete.on_click(board, f.get_name())
                    self.update_file_container()

    def update_file_container(self):
        self.files = ProjectManager.get_projects(self.theme)

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
            self.btn_select.color = self.theme.get("selection_background")
        else:
            self.btn_select.color = self.theme.get("button")
        if self.btn_delete.is_hovered(pg.mouse.get_pos()):
            self.btn_delete.color = self.theme.get("selection_background")
        else:
            self.btn_delete.color = self.theme.get("button")
