from flask import Flask


def create_app(config_file):
    a = Flask(__name__)
    # a.config.from_object(config_file)

    from api import api_general, api_python
    a.register_blueprint(api_general, url_prefix="/api")
    a.register_blueprint(api_python, url_prefix="/api/python")

    return a


if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=True,
            host="localhost",
            port="8001")
