from abc import ABC, abstractmethod
from utils.app_utils import DisplaySettings
import pygame as pg
from utils.gui_utils import Themes
from gui.buttons.apply_button import ApplyButton


class Form(ABC):

    def __init__(self, display, coords=None, size=None):
        ABC.__init__(self)
        self.display = display
        self.visible = False
        if size is None:
            self.size = (
                int(DisplaySettings.get_size_by_key()[0] * 0.45), int(DisplaySettings.get_size_by_key()[1] * .75))
        else:
            self.size = size
        if coords is None:
            self.coords = (int(DisplaySettings.get_size_by_key()[0] * .95 - self.size[0]),
                           int(DisplaySettings.get_size_by_key()[1] * .2))
        else:
            self.coords = coords
        self.btn_apply = ApplyButton(0)
        self.btn_apply.color = Themes.DEFAULT_THEME.get("panel_background")
        self.btn_apply.set_custom_coordinates(
            (int((self.coords[0] + self.size[0]) - self.btn_apply.get_rect().width * .53),
             int((self.coords[1] + self.size[1]) - self.btn_apply.get_rect().height * .6)))

    @abstractmethod
    def draw_form(self):
        self.update_form()
        if self.visible:
            self.btn_apply.set_custom_coordinates(
                (int((self.coords[0] + self.size[0]) - self.btn_apply.get_rect().width * .53),
                 int((self.coords[1] + self.size[1]) - self.btn_apply.get_rect().height * .6)))
            w = self.btn_apply.get_rect().width
            self.btn_apply.update_button(Themes.DEFAULT_THEME.get("panel_background"))
            if self.btn_apply.get_rect().width != w:
                self.btn_apply.set_custom_coordinates(
                    (int((self.coords[0] + self.size[0]) - self.btn_apply.get_rect().width * .53),
                     int((self.coords[1] + self.size[1]) - self.btn_apply.get_rect().height * .6)))
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("panel_background"), self.get_rect(), 0)
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("panel_front_light"), self.get_rect(), 3)
            pg.draw.rect(self.display, self.btn_apply.color, self.btn_apply.get_rect(), 0)
            self.display.blit(self.btn_apply.get_text(), self.btn_apply.get_text_rect())
            self.check_button_hover()

    def get_rect(self):
        return pg.Rect(self.coords, self.size)

    @abstractmethod
    def update_form(self, coords=None, size=None):
        if coords is None:
            self.coords = (int(DisplaySettings.get_size_by_key()[0] * .95 - self.size[0]),
                           int(DisplaySettings.get_size_by_key()[1] * .2))
        else:
            self.coords = coords
        if size is None:
            self.size = (
                int(DisplaySettings.get_size_by_key()[0] * 0.45), int(DisplaySettings.get_size_by_key()[1] * .75))
        else:
            self.size = size

    @abstractmethod
    def check_form_events(self, event):
        pass

    def check_button_hover(self):
        # BUTTON HOVERING
        if self.btn_apply.is_hovered(pg.mouse.get_pos()):
            self.btn_apply.color = Themes.DEFAULT_THEME.get("selection_background")
        else:
            self.btn_apply.color = Themes.DEFAULT_THEME.get("panel_background")
