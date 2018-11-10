from models.project import ProjectModel
from utils.enums.status import Status
from utils.managers.blueprint_manager import BlueprintManager
from utils.managers.manager import Manager


class ProjectManager(Manager):
    PROJECTS = list()

    @classmethod
    def create_project(cls, data):
        r = ProjectModel()
        r.name, r.api = data.get("NAME"), data.get("API")
        a, f, s, c = list(), list(), list(), list()
        for b in data.get("ATTRIBUTES"):
            a.append(BlueprintManager.call_parser(b))
        for b in data.get("FUNCTIONS"):
            f.append(BlueprintManager.call_parser(b))
        for b in data.get("SPRITES"):
            s.append(BlueprintManager.call_parser(b))
        for b in data.get("CHARACTERS"):
            c.append(BlueprintManager.call_parser(b))
        r.attributes = a
        r.functions = f
        r.sprites = s
        r.characters = s
        return r

    @classmethod
    def add_project(cls, project):
        r = Status.PROJECT_REGISTERED
        if len(ProjectManager.PROJECTS) > 0:
            for p in ProjectManager.PROJECTS:
                if p.name == project.name:
                    r = Status.PROJECT_EXISTS
                    break
            else:
                ProjectManager.PROJECTS.append(project)
        else:
            ProjectManager.PROJECTS.append(project)
        return r

    @classmethod
    def get_project(cls, name):
        r = ProjectModel()
        for p in ProjectManager.PROJECTS:
            if name == p.name:
                r = p
                r.status = Status.SUCCESS
                break
        else:
            r.status = Status.NOT_FOUND
        return r

    @classmethod
    def update_project(cls, project, data):
        s = Status.SUCCESS
        project.name = data.get("NAME")
        project.api = data.get("API")
        # CLEAR EXISTING DATA
        project.attributes.clear()
        project.functions.clear()
        project.sprites.clear()
        project.characters.clear()
        # UPDATE DATA
        for b in data.get("ATTRIBUTES"):
            project.add_attribute(BlueprintManager.call_parser(b))
        for b in data.get("FUNCTIONS"):
            project.add_function(BlueprintManager.call_parser(b))
        for b in data.get("SPRITES"):
            project.add_sprite(BlueprintManager.call_parser(b))
        for b in data.get("CHARACTERS"):
            project.add_character(BlueprintManager.call_parser(b))
        return s
