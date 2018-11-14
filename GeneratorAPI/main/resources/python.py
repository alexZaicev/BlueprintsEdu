import json

import flask_restful
from flask import send_file

from models.entity import Entity
from utils import logger_utils
from utils.enums.status import Status
from utils.generators.python_generator import PythonGenerator
from utils.managers.download_manager import DownloadManager
from utils.managers.project_manager import ProjectManager

LOGGER = logger_utils.get_logger(__name__)


class Info(flask_restful.Resource):

    def get(self):
        """Description: Helper GET call to list all Python specific API calls in Generator

        :return: Dictionary with path and description values
        """
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
        p = ProjectManager.get_project(name)
        e = Entity()
        if p is not None:
            e.status = PythonGenerator.generate(p)
        else:
            e.status = Status.GENERATION_FAILED
        return e.to_dict()


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
        if isinstance(flask_restful.request.get_json(), str):
            data = json.loads(flask_restful.request.get_json())
        elif isinstance(flask_restful.request.get_json(), dict):
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
        if isinstance(flask_restful.request.get_json(), str):
            data = json.loads(flask_restful.request.get_json())
        elif isinstance(flask_restful.request.get_json(), dict):
            data = flask_restful.request.get_json()
        else:
            data = dict()
        e.status = ProjectManager.update_project(p, data)
        return e.to_dict()


class DownloadProject(flask_restful.Resource):

    def get(self, name, compression):
        """Description: GET download generated project files as zip archive

        :param name: Name of the generated project
        :param compression: Archive compression type: zip or tar
        :return: Project archive of archive type passed in
        """
        archive_path = DownloadManager.get_project_archive(name, compression)
        if archive_path is not None:
            return send_file(filename_or_fp=archive_path, attachment_filename="{}.{}".format(name, compression),
                             as_attachment=True)
