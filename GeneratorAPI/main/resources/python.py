import flask_restful

from models.entity import Entity
from utils import logger_utils
from utils.enums.status import Status
from utils.managers.project_manager import ProjectManager

LOGGER = logger_utils.get_logger(__name__)


class Info(flask_restful.Resource):

    def get(self):
        r = dict()
        r["/api/python"] = "GET: General API information containing python specific calls"
        r["/api/python/generate"] = "POST: Python code generator from blueprint json strings"
        e = Entity(status=Status.SUCCESS, data=r)
        return e.to_dict()


class Generate(flask_restful.Resource):

    def get(self, name):
        """Description: GET generate python project from registered project

        :param name: Project name to generate from
        :return: Entity object with request status
        """
        pass


class Project(flask_restful.Resource):

    def get(self, name=None):
        """Description: GET single project by name or all registered projects

        :param name: <<Optional>> project name
        :return: Project JSON response
        """
        if name is None:
            r = list()
            for p in ProjectManager.PROJECTS:
                r.append(p.to_dict())
        else:
            r = ProjectManager.get_project(name)
            r = r.to_dict()

        e = Entity(status=Status.SUCCESS, data=r)
        return e.to_dict()

    def post(self):
        """Description: POST register project

        :return: Registration status
        """
        e = Entity()
        data = flask_restful.request.get_json()
        p = ProjectManager.create_project(data)
        e.status = ProjectManager.add_project(p)
        return e.to_dict()

    def put(self, name):
        """Description: PUT updates project and it`s content

        :param name: Project name
        :return: Request status
        """
        e = Entity()
        p = ProjectManager.get_project(name)
        e.status = ProjectManager.update_project(p, flask_restful.request.get_json())
        return e.to_dict()


class DownloadProject(flask_restful.Resource):

    def get(self, name):
        """Description: GET download generated project files as zip archive

        :param name: Name of the generated project
        :return: Project Zip archive
        """
        return None
