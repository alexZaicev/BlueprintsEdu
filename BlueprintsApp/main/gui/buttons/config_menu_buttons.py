from gui.buttons.button import Button
from utils.gui_utils import Themes
from utils.string_utils import StringUtils


class LanguageButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_LANGUAGE"), pos)

    def on_click(self, board, form=None):
        super().on_click(board)

    def update_button(self, text=None, color=Themes.DEFAULT_THEME.get("button")):
        if text is None:
            text = StringUtils.get_string("ID_LANGUAGE")
        super().update_button(text, color)


class ThemeButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_THEME"), pos)

    def on_click(self, board, form=None):
        super().on_click(board)

    def update_button(self, text=None, color=Themes.DEFAULT_THEME.get("button")):
        if text is None:
            text = StringUtils.get_string("ID_THEME")
        super().update_button(text, color)


class DisplayButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_DISPLAY"), pos)

    def on_click(self, board, form=None):
        super().on_click(board)

    def update_button(self, text=None, color=Themes.DEFAULT_THEME.get("button")):
        if text is None:
            text = StringUtils.get_string("ID_DISPLAY")
        super().update_button(text, color)
