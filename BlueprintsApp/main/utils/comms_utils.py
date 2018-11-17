import json
import os
import platform
import zipfile
from http import HTTPStatus

import requests

from utils import logger_utils
from utils.app_utils import DownloadError
from utils.enums.status import Status
from utils.managers.project_manager import ProjectManager
from utils.utils import Utils


class CommsUtils(Utils):
    HOST = "http://127.0.0.1"
    PORT = 8001
    ROOT = '/api'
    ROOT_PATH = "{}:{}{}".format(HOST, PORT, ROOT)
    __LOGGER = logger_utils.get_logger(__name__)

    @classmethod
    def get(cls, path):
        """Description: GET method request data from API and returns JSON response

        :param path: API endpoint
        :return: None - if error occurred OR dictionary of the parsed JSON response
        """
        data = None
        r = requests.get("{}{}".format(CommsUtils.ROOT_PATH, path))
        if r.status_code == HTTPStatus.OK:
            data = r.json()
        else:
            CommsUtils.__LOGGER.error("Something went wrong while making request to the API: {}".format(r.status_code))
        return data

    @classmethod
    def post(cls, path, data_send):
        """Descriptions: POST method sends data to the API and receives action response back

        :param path: API endpoint
        :param data_send: Dictionary of data to send
        :return: None - if error occurred OR dictionary of the parsed JSON response
        """
        data = None
        r = requests.post("{}{}".format(CommsUtils.ROOT_PATH, path), json=data_send)
        if r.status_code == HTTPStatus.OK:
            data = r.json()
        else:
            CommsUtils.__LOGGER.error("Something went wrong while making request to the API: {}".format(r.status_code))

        return data

    @classmethod
    def put(cls, path, data_send):
        """Description: PUT method updates already existing data in the API and receives
        request action response

        :param path: API endpoint
        :param data_send: Dictionary of data to send
        :return: None - if error occurred OR dictionary of the parsed JSON response
        """
        data = None
        r = requests.put("{}{}".format(CommsUtils.ROOT_PATH, path), json=data_send)
        if r.status_code == HTTPStatus.OK:
            data = r.json()
        else:
            CommsUtils.__LOGGER.error(
                "Something went wrong while making request to the API: {}".format(r.status_code))
        return data

    @classmethod
    def build_project_model(cls, name, api, characters=None, attributes=None, functions=None, sprites=None):
        """Description: Method build JSON object that is understandable on the API endpoint

        :param name: Project name
        :param api: Project API used
        :param characters: List of characters
        :param attributes: List of attributes
        :param functions: List of functions
        :param sprites: List of sprites
        :return: parsed JSON object
        """
        r = dict()
        r["NAME"] = name
        r["API"] = api
        if characters is None:
            r["CHARACTERS"] = list()
        else:
            ls = list()
            for c in characters:
                ls.append(c.to_dict())
            r["CHARACTERS"] = ls
        if attributes is None:
            r["ATTRIBUTES"] = list()
        else:
            ls = list()
            for a in attributes:
                ls.append(a.to_dict())
            r["ATTRIBUTES"] = ls
        if functions is None:
            r["FUNCTIONS"] = list()
        else:
            ls = list()
            for f in functions:
                ls.append(f.to_dict())
            r["FUNCTIONS"] = ls
        if sprites is None:
            r["SPRITES"] = list()
        else:
            ls = list()
            for s in sprites:
                ls.append(s.to_dict())
            r["SPRITES"] = ls
        return json.dumps(r)

    @classmethod
    def download_project(cls, name):
        compressions = {
            "Darwin": "",
            "Windows": "zip",
            "Linux": "tar"
        }
        ext = compressions.get(platform.system())
        path = "{}/python/download/{}/{}".format(CommsUtils.ROOT_PATH, name, ext)
        resp = requests.get(path, allow_redirects=True)
        if resp.status_code == HTTPStatus.OK:
            out_path = "{}{}\\out".format(ProjectManager.PATH, name)
            zip_path = "{}\\{}.{}".format(out_path, name, ext)
            if not os.path.exists(out_path):
                os.mkdir(out_path)
            else:
                if os.path.exists(zip_path):
                    os.remove(zip_path)

            if os.path.exists("{}{}".format(ProjectManager.PATH, name)):
                with open(zip_path, "wb+") as f:
                    f.write(resp.content)
                zip_file = zipfile.ZipFile(zip_path, "r")
                zip_file.extractall(path="{}{}\\out\\".format(ProjectManager.PATH, name))
                zip_file.close()

                os.remove(zip_path)
            else:
                CommsUtils.__LOGGER.error("Project [{}] directory does not exists".format(name))
                raise FileNotFoundError("Failed to save generated source code")
        else:
            CommsUtils.__LOGGER.error("Failed to download project [{}] from [{}]".format(name, path))
            raise DownloadError("Failed to download project [{}]".format(name))
        return Status.SUCCESS
