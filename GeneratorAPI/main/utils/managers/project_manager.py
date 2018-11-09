from utils.managers.manager import Manager
from utils.enums.status import Status
from models.project import ProjectModel


class ProjectManager(Manager):
    PROJECTS = list()

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
            project.add_attribute(b)
        for b in data.get("FUNCTIONS"):
            project.add_function(b)
        for b in data.get("SPRITES"):
            project.add_sprite(b)
        for b in data.get("CHARACTERS"):
            project.add_character(b)
        return s
