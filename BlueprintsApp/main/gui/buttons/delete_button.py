from gui.buttons.button import Button
from utils.string_utils import StringUtils
from project_manager import ProjectManager


class DeleteButton(Button):

    def __init__(self, pos):
        Button.__init__(self, StringUtils.get_string("ID_DELETE"), pos)

    def on_click(self, board, directory):
        ProjectManager.delete_project(directory)
        super().on_click(board)

    def update_button(self):
        super().update_button(StringUtils.get_string("ID_DELETE"))
