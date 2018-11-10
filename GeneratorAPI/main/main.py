from flask import Flask
from flask_jwt_extended import JWTManager


def create_app(config_file=None):
    a = Flask(__name__)
    if config_file is not None:
        a.config.from_object(config_file)

    from api import api_general, api_python, api_auth
    a.register_blueprint(api_general, url_prefix="/api")
    a.register_blueprint(api_python, url_prefix="/api/python")
    a.register_blueprint(api_auth, url_prefix="/api")
    return a


if __name__ == "__main__":
    app = create_app("config")
    jwt = JWTManager(app)
    app.run(debug=True,
            host="localhost",
            port="8001")
