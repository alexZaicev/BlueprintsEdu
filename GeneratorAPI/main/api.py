"""
    Description: api module contains all registered REST-ful API resources, blueprint and
    paths to them
"""

from flask import Blueprint
from flask_restful import Api
from resources.info import *


api_bp = Blueprint("GeneratorAPI", __name__)
api = Api(api_bp)

api.add_resource(Help, "/help")

