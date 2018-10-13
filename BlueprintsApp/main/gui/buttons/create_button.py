from gui.buttons.button import Button
from utils.string_utils import StringUtils
from utils import scene_utils
from project_manager import ProjectManager


class CreateButton(Button):

    def __init__(self, theme, pos):
        Button.__init__(self, StringUtils.get_string("ID_CREATE"), theme, pos)

    def on_click(self, board, project_info):
        ProjectManager.create_project(project_info)
        board.set_scene(scene_utils.DEVELOP_SCENE, project=project_info)
        super().on_click(board)
