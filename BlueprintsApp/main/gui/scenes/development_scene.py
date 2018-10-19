from gui.scenes.scene_builder import SceneBuilder
from utils import logger_utils
from utils.gui_utils import Themes
from gui.buttons.dev_file_button import DevFileButton
from gui.buttons.dev_run_button import DevRunButton
from gui.buttons.dev_settings_button import DevSettingsButton
import pygame as pg
from utils import app_utils, gui_utils
from utils.string_utils import StringUtils


class DevelopmentScene(SceneBuilder):

    def __init__(self, display, project):
        SceneBuilder.__init__(self, display)
        self.__logger = logger_utils.get_logger(__name__)
        self.__project = project
        self.__logger.debug("{} --- {}".format(project[0], project[1]))
        pg.display.set_caption("{} - {}   {}".format(project[0], project[1], app_utils.CAPTION))
        self.btn_file = DevFileButton(0)
        self.btn_file.color = Themes.DEFAULT_THEME.get("background")
        self.btn_run = DevRunButton(0)
        self.btn_run.color = Themes.DEFAULT_THEME.get("background")
        self.btn_settings = DevSettingsButton(0)
        self.btn_settings.color = Themes.DEFAULT_THEME.get("background")
        self.__cont_panel = None
        self.__bp_panel = None
        self.__bp_focused = False
        self.__init_btn_coords()

    def __init_btn_coords(self):
        self.btn_settings.set_custom_coordinates(
            (int(app_utils.BOARD_WIDTH - self.btn_settings.get_rect().width * .5),
            int(0 + self.btn_settings.get_rect().height * .5)))
        self.btn_run.set_custom_coordinates(
            (int(self.btn_settings.get_rect().left - (self.btn_run.get_rect().width * .5
                + app_utils.BOARD_WIDTH * gui_utils.BUTTON_MENU_MARGIN)),
            int(0 + self.btn_run.get_rect().height * .5)))
        self.btn_file.set_custom_coordinates((
            int(self.btn_run.get_rect().left - (self.btn_file.get_rect().width * .5
                + app_utils.BOARD_WIDTH * gui_utils.BUTTON_MENU_MARGIN)),
            int(0 + self.btn_file.get_rect().height * .5)
        ))

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

    def draw_control_panel (self):
        self.__cont_panel = pg.Rect((int(app_utils.BOARD_WIDTH * .005), int(app_utils.BOARD_HEGHT * .005)),
        (int(app_utils.BOARD_WIDTH * .265), int(app_utils.BOARD_HEGHT * .99)))
        if self.__bp_focused:
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("panel_background"), self.__cont_panel, 0)
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("selection_background"), self.__cont_panel, 2)
        else:
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("panel_disabled"), self.__cont_panel, 0)
        font = pg.font.Font(Themes.DEFAULT_THEME.get("text_font_style"), int(self.__cont_panel.width * .15))
        txt = font.render(StringUtils.get_string("ID_CONTROL_PANEL"), True, Themes.DEFAULT_THEME.get("font"))
        rect_txt = txt.get_rect()
        rect_txt.topleft = (int(self.__cont_panel.centerx - rect_txt.width * .5), int(self.__cont_panel.top + self.__cont_panel.top * .015))
        self.display.blit(txt, rect_txt)

    def draw_blueprint_control(self):
        self.__bp_panel = pg.Rect((int(self.__cont_panel.right + app_utils.BOARD_WIDTH * .005), int(self.btn_file.get_rect().bottom * 1.05)),
            (int(app_utils.BOARD_WIDTH * .723),
                int(app_utils.BOARD_HEGHT * (1.0 - gui_utils.BUTTON_PRIMARY[1] - .007))))
        pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("panel_background"), self.__bp_panel, 0)
        pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("selection_background"), self.__bp_panel, 2)

    def draw_scene(self):
        # PREPARE DATA
        # DISPLAY
        self.display.fill(Themes.DEFAULT_THEME.get("background"))
        self.draw_menu_buttons()
        self.draw_control_panel()
        self.draw_blueprint_control()
        super().draw_scene()

    def check_button_hover(self):
        if self.btn_settings.is_hovered(pg.mouse.get_pos()):
            self.btn_settings.color = Themes.DEFAULT_THEME.get("selection_background")
        else:
            self.btn_settings.color = Themes.DEFAULT_THEME.get("background")
        if self.btn_run.is_hovered(pg.mouse.get_pos()):
            self.btn_run.color = Themes.DEFAULT_THEME.get("selection_background")
        else:
            self.btn_run.color = Themes.DEFAULT_THEME.get("background")
        if self.btn_file.is_hovered(pg.mouse.get_pos()):
            self.btn_file.color = Themes.DEFAULT_THEME.get("selection_background")
        else:
            self.btn_file.color = Themes.DEFAULT_THEME.get("background")

    def check_events(self, event, board):
        super().check_events(event, board)
