import datetime
import json
import os
import shutil
import time

from project import Project
from utils import logger_utils
from utils.managers.blueprint_manager import BlueprintManager
from utils.managers.manager import Manager
from utils.managers.security_manager import SecurityManager


class ProjectManager(Manager):
    LOGGER = logger_utils.get_logger(__name__)
    PATH = logger_utils.ROOT_PATH + "BlueprintsApp\projects\\"
    PROJECT_FILE_EXTENSION = ".blue"
    BLUEPRINT_FILE_EXTENSION = ".bp"

    @classmethod
    def get_projects(cls):
        result = []
        ProjectManager.LOGGER.info("Fetching Existing Projects")
        if not os.path.exists(ProjectManager.PATH):
            try:
                ProjectManager.LOGGER.error("Projects directory not found")
                ProjectManager.LOGGER.info("Creating new projects directory")
                os.makedirs(ProjectManager.PATH)
            except OSError as ex:
                ProjectManager.LOGGER.error("Failed to create projects directory")
        if len(os.listdir(ProjectManager.PATH)) > 0:
            dirs = [directory for directory in os.listdir(ProjectManager.PATH)
                    if os.path.isdir(os.path.join(ProjectManager.PATH, directory)) and
                    ProjectManager.is_valid_project(ProjectManager.PATH + directory)
                    ]
            for directory in dirs:
                t = time.ctime(max(os.path.getmtime(root) for root, _, _ in os.walk(ProjectManager.PATH + directory)))
                result.append(Project(directory, str(datetime.datetime.strptime(
                    t, "%a %b %d %H:%M:%S %Y"))))
        else:
            raise FileNotFoundError("No saved projects exists")
        return result

    @classmethod
    def get_project_info(cls, project_name):
        api = ""
        bps, bp_conns = None, None
        try:
            fname = "{}{}\{}{}".format(ProjectManager.PATH, project_name, project_name.lower(),
                                       ProjectManager.PROJECT_FILE_EXTENSION)
            with open(fname, "rb") as file:
                dt = SecurityManager.decode_data(file.read())
                content = json.loads(dt)
                if project_name == content.get("PROJECT_NAME"):
                    api = content.get("PROJECT_API")
                    generated = content.get("GENERATED")
                    bp_conns = content.get("CONNECTIONS")
                    bps = ProjectManager.get_project_files("{}{}".format(ProjectManager.PATH, project_name))
                    ProjectManager.LOGGER.debug(bp_conns)
                    ProjectManager.LOGGER.debug(bps)
                else:
                    ProjectManager.LOGGER.critical(
                        "Failed to load project. Unknown project name [{}]".format(project_name))
                    # TODO close application after critical error
        except OSError as ex:
            ProjectManager.LOGGER.error("Failed to get project files [{}]".format(project_name))
        return {
            "PROJECT_NAME": project_name,
            "PROJECT_API": api,
            "GENERATED": generated,
            "CONNECTIONS": bp_conns,
            "BLUEPRINTS": bps
        }

    @classmethod
    def create_project(cls, data):
        d = dict()
        d["PROJECT_NAME"] = data.get("PROJECT_NAME")
        d["PROJECT_API"] = data.get("PROJECT_API")
        d["GENERATED"] = False
        d["CONNECTIONS"] = list()

        if not os.path.exists(ProjectManager.PATH):
            ProjectManager.LOGGER.warning("Unable to find projects directory...")
            ProjectManager.LOGGER.info("Creating new projects directory...")
            os.mkdir(ProjectManager.PATH)

        path = "{}{}".format(ProjectManager.PATH, data.get("PROJECT_NAME"))
        if not os.path.exists(path):
            os.mkdir(path)
        else:
            raise FileExistsError("Cannot override already existing project [{}]".format(data.get("PROJECT_NAME")))

        with open("{}\{}{}".format(path, data.get("PROJECT_NAME").lower(), ProjectManager.PROJECT_FILE_EXTENSION),
                  "wb+") as file:
            dt = SecurityManager.encode_data(json.dumps(d))
            file.write(dt)

    @classmethod
    def is_valid_project(cls, dir):
        check = False
        try:
            files = [file for file in os.listdir(dir)
                     if file.endswith(ProjectManager.PROJECT_FILE_EXTENSION)
                     ]
            if len(files) != 1:
                ProjectManager.LOGGER.error("Invalid project found {}".format(dir))
            else:
                check = True
        except OSError as ex:
            ProjectManager.LOGGER.error("Failed to check project directories")
        return check

    @classmethod
    def get_project_files(cls, directory):
        fs = list()
        for root, dirs, files in os.walk(directory):
            for f in files:
                if f.endswith(ProjectManager.BLUEPRINT_FILE_EXTENSION):
                    fs.append("{}\{}".format(directory, f))
        content = list()
        for f in fs:
            with open(f, "rb") as c:
                dt = c.read()
                dt = SecurityManager.decode_data(dt)
                content.append(json.loads(dt))
        return content

    @classmethod
    def save_project(cls, project_name, bp_data, bp_conns, generated):
        bp_content, bp_conns_content = BlueprintManager.parse_blueprints(bp_data, bp_conns)
        ProjectManager.LOGGER.debug("BP content: {}".format(bp_content))
        ProjectManager.LOGGER.debug("BPS connections: {}".format(bp_conns_content))
        # PROJECT FILE
        r = dict()
        r["PROJECT_NAME"], r["PROJECT_API"] = project_name
        r["GENERATED"] = generated
        r["CONNECTIONS"] = bp_conns_content

        f_name = "{}{}\{}{}".format(ProjectManager.PATH, project_name[0],
                                    project_name[0].lower(), ProjectManager.PROJECT_FILE_EXTENSION)
        with open(f_name, "wb+") as f:
            r = json.dumps(r)
            f.write(SecurityManager.encode_data(r))
        # BLUEPRINT DATA
        for k, v in bp_content.items():
            f_name = "{}{}\{}{}".format(ProjectManager.PATH, project_name[0],
                                        k.lower(), ProjectManager.BLUEPRINT_FILE_EXTENSION)
            with open(f_name, "wb+") as f:
                e_data = SecurityManager.encode_data(v)
                f.write(e_data)

    @classmethod
    def delete_project(cls, directory):
        ProjectManager.LOGGER.debug("Directory: " + directory)
        if os.path.isdir(os.path.join(ProjectManager.PATH, directory)):
            shutil.rmtree(ProjectManager.PATH + directory)
            ProjectManager.LOGGER.debug("Directory: " + directory + " deleted")
