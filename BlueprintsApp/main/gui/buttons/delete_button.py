from gui.buttons.button import Button
from utils.string_utils import StringUtils
from project_manager import ProjectManager
from utils.gui_utils import Themes


class DeleteButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_DELETE"), pos)

    def on_click(self, board, directory=None, form=None):
        super().on_click(board)
        if directory is not None:
            ProjectManager.delete_project(directory)

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_DELETE"), color)
