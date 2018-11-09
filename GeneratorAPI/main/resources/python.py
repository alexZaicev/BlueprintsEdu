from flask_restful import Resource, request
from utils.managers.project_manager import ProjectManager
from models.project import ProjectModel
from models.entity import Entity


class Info(Resource):

    def get(self):
        r = dict()
        r["/api/python"] = "GET: General API information containing python specific calls"
        r["/api/python/generate"] = "POST: Python code generator from blueprint json strings"
        return r


class Generate(Resource):

    def get(self, name):
        """Description: GET generate python project from registered project

        :param name: Project name to generate from
        :return: Entity object with request status
        """
        pass


class Project(Resource):

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
        return r

    def post(self):
        """Description: POST register project

        :return: Registration status
        """
        e = Entity()
        data = request.get_json()
        a, c, f, s = data.get("ATTRIBUTES"), data.get("CHARACTERS"), data.get("FUNCTIONS"), data.get("SPRITES")
        p = ProjectModel(name=data.get("NAME"), api=data.get("API"), attributes=a, characters=c, functions=f, sprites=s)
        e.project = p.name
        e.api = p.api
        e.status = ProjectManager.add_project(p)
        return e.to_dict()

    def put(self, name):
        """Description: PUT updates project and it`s content

        :param name: Project name
        :return: Request status
        """
        e = Entity()
        p = ProjectManager.get_project(name)
        e.status = ProjectManager.update_project(p, request.get_json())
        e.project = p.name
        e.api = p.api
        return e.to_dict()


class DownloadProject(Resource):

    def get(self, name):
        """Description: GET download generated project files as zip archive

        :param name: Name of the generated project
        :return: Project Zip archive
        """
        return None
