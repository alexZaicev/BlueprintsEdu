from gui.buttons.button import Button
from utils.string_utils import StringUtils
from utils import scene_utils
from project_manager import ProjectManager


class SelectButton(Button):

    def __init__(self, pos):
        Button.__init__(self, StringUtils.get_string("ID_SELECT"), pos)

    def on_click(self, board, project):
        board.set_scene(scene_utils.DEVELOP_SCENE, ProjectManager.get_project_info(project))
        super().on_click(board)
