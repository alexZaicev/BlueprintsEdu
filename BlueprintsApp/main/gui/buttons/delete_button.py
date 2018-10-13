from gui.buttons.button import Button
from utils.string_utils import StringUtils
from project_manager import ProjectManager

class DeleteButton(Button):

    def __init__(self, theme, pos):
        Button.__init__(self, StringUtils.get_string("ID_DELETE"), theme, pos)

    def on_click(self, board, directory):
        ProjectManager.delete_project(directory)
        super().on_click(board)
