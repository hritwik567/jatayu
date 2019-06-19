import os

from flask import Flask
from flask_cors import CORS

from .main import Handler


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # enable CORS
    CORS(app)

    @app.route("/")
    def ctx():
        return Handler()

    return app
