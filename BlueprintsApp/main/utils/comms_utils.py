from utils.utils import Utils
import requests
from http import HTTPStatus
import json
from utils import logger_utils


class CommsUtils(Utils):
    HOST = "127.0.0.1"
    PORT = 8001
    ROOT = '/api'
    ROOT_PATH = "{}{}{}".format(HOST, PORT, ROOT)
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
            try:
                data = json.loads(r.json())
            except ValueError as ex:
                CommsUtils.__LOGGER.error(
                    "Error occurred while trying to decode JSON response: {}".format(str(ex)))
                CommsUtils.__LOGGER.debug("RECEIVED DATA: {}".format(data))
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
        r = requests.post("{}{}".format(CommsUtils.ROOT_PATH, path), data=data_send)
        if r.status_code == HTTPStatus.OK:
            try:
                data = json.loads(r.json())
            except ValueError as ex:
                CommsUtils.__LOGGER.error(
                    "Error occurred while trying to decode JSON response: {}".format(str(ex)))
                CommsUtils.__LOGGER.debug("RECEIVED DATA: {}".format(data))
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
        r = requests.put("{}{}".format(CommsUtils.ROOT_PATH, path), data=data_send)
        if r.status_code == HTTPStatus.OK:
            try:
                data = json.loads(r.json())
            except ValueError as ex:
                CommsUtils.__LOGGER.error(
                    "Error occurred while trying to decode JSON response: {}".format(str(ex)))
                CommsUtils.__LOGGER.debug("RECEIVED DATA: {}".format(data))
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
