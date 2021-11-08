"""Main Flask application."""

import random
import typing as t

import flask


def get_data(name: t.Optional[str]) -> t.Mapping[str, int]:
    """Obtain data from *somewhere*."""
    if name:
        return {f"{name}_x": random.randint(1, 4), f"{name}_y": random.randint(1, 4)}
    else:
        return {"x": random.randint(1, 4), "y": random.randint(1, 4)}


def create_app() -> flask.Flask:
    """Create the Flask instance."""

    # __name__ is a python module-level constant
    # that lets flask locate the project in the file system
    app = flask.Flask(__name__)

    @app.route("/")
    def _index() -> str:
        return "<p>Hello world</p>"

    @app.route("/data", defaults={"name": None})
    @app.route("/data/<name>")
    def _data(name: t.Optional[str]) -> flask.Response:
        return flask.jsonify(get_data(name))

    return app
