from gui.buttons.button import Button
from utils import scene_utils
from utils.gui_utils import Themes
from utils.managers.project_manager import ProjectManager
from utils.string_utils import StringUtils


class SelectButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_SELECT"), pos)

    def on_click(self, board, project=None, form=None):
        super().on_click(board)
        if project is not None:
            board.set_scene(scene_utils.DEVELOP_SCENE, ProjectManager.get_project_info(project))

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_SELECT"), color)
