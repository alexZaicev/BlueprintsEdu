from gui.buttons.button import Button
from utils.string_utils import StringUtils
from utils.enums import status
from utils.gui_utils import Themes


class ExitButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_EXIT"), pos)

    def on_click(self, board):
        board.app_status = status.EXIT
        super().on_click(board)

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_EXIT"), color)
