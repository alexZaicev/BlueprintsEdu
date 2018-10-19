from gui.buttons.button import Button
from utils.string_utils import StringUtils
from utils.gui_utils import Themes


class DevFileButton(Button):

    def __init__(self, pos):
        Button.__init__(self, StringUtils.get_string("ID_FILE"), pos)

    def on_click(self, event, board):
        super().on_click(event, board)

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_FILE"), color)
