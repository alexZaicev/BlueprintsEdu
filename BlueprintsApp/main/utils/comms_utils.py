from utils.utils import Utils
import requests
from http import HTTPStatus


class CommsUtils(Utils):

    HOST = "127.0.0.1"
    PORT = 8001
    ROOT = '/api'
    ROOT_PATH = "{}{}{}".format(HOST, PORT, ROOT)

    @classmethod
    def get(cls, path):
        r = requests.get("{}{}".format(CommsUtils.ROOT_PATH, path))
        if r.status_code == HTTPStatus.OK:
            pass

    @classmethod
    def post(cls, obj):
        pass
