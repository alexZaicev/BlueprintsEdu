from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token

from models.entity import Entity
from utils.enums.status import Status
import json

# with open("users.config", "r") as f:
#     USERS = json.load(f).get("USERS")


class Login(Resource):

    def post(self):
        e = Entity()
        if not request.is_json:
            e.status = Status.FAILED
            e.data = {
                "MESSAGE": "Missing JSON request body"
            }
            return e.to_dict(), 400
        usr = request.json.get("USERNAME", None)
        pwd = request.json.get("PASSWORD", None)
        if usr is None or pwd is None:
            e.status = Status.FAILED
            e.data = {
                "MESSAGE": "Missing one of the login parameters",
                "USERNAME": usr,
                "PASSWORD": pwd
            }
            return e.to_dict(), 400
        else:
            for u in USERS:
                if u.get("USERNAME") == usr and u.get("PASSWORD") == pwd:
                    token = create_access_token(identity=usr)
                    e.status = Status.SUCCESS
                    e.data = {
                        "TOKEN": token
                    }
                    break
            else:
                e.status = Status.SUCCESS
                e.data = {
                    "MESSAGE": "User is not authorized to access API"
                }

        return e.to_dict(), 200

