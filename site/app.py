"""Main Flask application."""

import random
import typing as t

import flask
import requests

# def get_data(name: t.Optional[str]) -> t.Mapping[str, int]:
#     """Obtain data from *somewhere*."""
#     if name:
#         return {f"{name}_x": random.randint(1, 4), f"{name}_y": random.randint(1, 4)}
#     else:
#         return {"x": random.randint(1, 4), "y": random.randint(1, 4)}


def create_app() -> flask.Flask:
    """Create the Flask instance."""

    # __name__ is a python module-level constant
    # that lets flask locate the project in the file system
    app = flask.Flask(__name__)

    @app.route("/")
    # def _index() -> str:
    #     return "<p>Hello world</p>"

    def _index() -> flask.render_template:
        return flask.render_template("index.html")

    @app.route("/profile")
    def _profile() -> flask.render_template:
        return flask.render_template("profile.html")

    @app.route("/quiz")
    def _quiz() -> flask.render_template:
        return flask.render_template("quiz.html")

    # @app.route("/data", defaults={"name": None})
    # @app.route("/data/<name>")
    # def _data(name: t.Optional[str]) -> flask.Response:
    #     return flask.jsonify(get_data(name))

    @app.route("/test")
    def _test() -> str:
        """Testing endpoint."""
        return "<br>".join(
            [
                flask.request.base_url,
                flask.request.host,
                flask.request.host_url,
            ]
        )

    @app.route("/data")
    def _data() -> flask.Response:
        """Normal data."""
        return flask.jsonify({"x": 1})

    @app.route("/cooler_data")
    def _cooler() -> flask.Response:
        """Cooler data."""
        # also look into requests.Session
        # for bulk requests

        # gets base URL, e.g. 'http://localhost:5000/'
        base_url = flask.request.host_url
        endpoint = base_url + "data"
        # make request
        resp = requests.get(endpoint)
        # parse response
        data = resp.json()
        cooler_data = {"y": data["x"] + 1}
        # return response
        return flask.jsonify(cooler_data)

    return app
