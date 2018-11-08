from flask import Flask


def create_app(config_file):
    a = Flask(__name__)
    # a.config.from_object(config_file)

    from api import api_bp
    a.register_blueprint(api_bp, url_prefix="/api")

    return a


if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=True,
            host="localhost",
            port="8001")
