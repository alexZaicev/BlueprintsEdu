from gui.buttons.button import Button
from utils.enums.status import Status
from utils.gui_utils import Themes
from utils.string_utils import StringUtils


class ExitButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_EXIT"), pos)

    def on_click(self, board, form=None):
        board.app_status = Status.EXIT
        super().on_click(board)

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_EXIT"), color)
