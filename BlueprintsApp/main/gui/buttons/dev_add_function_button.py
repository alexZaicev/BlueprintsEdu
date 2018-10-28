from gui.buttons.button import Button
from utils.string_utils import StringUtils
from utils.gui_utils import Themes


class DevAddFunctionButton(Button):

    def __init__(self, pos):
        Button.__init__(self, StringUtils.get_string("ID_ADD_FUNCTION"), pos)

    def on_click(self, board, form):
        super().on_click(board)
        form.add_function()

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_ADD_FUNCTION"), color)
