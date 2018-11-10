"""
    Description: api module contains all registered REST-ful API resources, blueprint and
    paths to them
"""

from flask import Blueprint
from flask_restful import Api

from resources.authentication import *
from resources.info import *
from resources.python import *
from utils.enums.status import Status


api_general = Blueprint("general", __name__)
api_python = Blueprint("python", __name__)
api_auth = Blueprint("auth", __name__)

general = Api(api_general)
python_generator = Api(api_python)
auth = Api(api_auth)

routes = ["", "/", "/help"]
# GENERAL
general.add_resource(Help, *routes)

# AUTHENTICATION
auth.add_resource(Login, "/login")

# PYTHON SPECIFIC
python_generator.add_resource(Info, *routes)
routes = ["/project", "/project/<string:name>"]
python_generator.add_resource(Project, *routes)
python_generator.add_resource(Generate, "/generate/<string:name>")

"""
Description: API error handling
"""


@api_general.errorhandler(TypeError)
@api_python.errorhandler(TypeError)
def handle_type_error(error):
    return str({
        "message": Status.INVALID_API_CALL,
        "error": str(error)
    }), 404


@api_general.errorhandler(AttributeError)
@api_python.errorhandler(AttributeError)
def handle_type_error(error):
    return str({
        "message": Status.BAD_REQUEST,
        "error": str(error)
    }), 400
