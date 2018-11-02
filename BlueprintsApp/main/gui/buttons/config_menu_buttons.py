from gui.buttons.button import Button
from utils.string_utils import StringUtils
from utils.gui_utils import Themes


class LanguageButton(Button):

    def __init__(self, pos):
        Button.__init__(self, StringUtils.get_string("ID_LANGUAGE"), pos)

    def on_click(self, board):
        super().on_click(board)

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_LANGUAGE"), color)


class ThemeButton(Button):

    def __init__(self, pos):
        Button.__init__(self, StringUtils.get_string("ID_THEME"), pos)

    def on_click(self, board):
        super().on_click(board)

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_THEME"), color)
