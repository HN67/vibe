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


def api_url(name: str) -> str:
    """Construct an absolute API URL from a relative URL.

    For example, if the site is running on http localhost:5000,
    api_url(flask.request, 'moods/happy') == http://localhost:5000/api/moods/happy
    """
    return flask.request.host_url + "/api/" + name


def create_app() -> flask.Flask:
    """Create the Flask instance."""

    # __name__ is a python module-level constant
    # that lets flask locate the project in the file system
    app = flask.Flask(__name__)

    @app.route("/")
    # def _index() -> str:
    #     return "<p>Hello world</p>"

    def _index() -> str:
        return flask.render_template("index.html")

    @app.route("/profile/testuser")
    def _profile() -> str:
        return flask.render_template("profile.html")

    @app.route("/login", methods=["GET", "POST"])
    def _login():
        error = None
        if flask.request.method == "POST":
            if flask.request.form["username"] != "testuser":
                error = "Invalid Credentials. Please try again."
            else:
                return flask.redirect(flask.url_for("_profile"))
        return flask.render_template("login.html", error=error)

    @app.route("/quiz", methods=["GET", "POST"])
    def _quiz() -> str:
        if flask.request.method == "POST":
            if flask.request.form.get("v"):
                return flask.redirect(flask.url_for("_result"))
            elif flask.request.form.get("vands"):
                return flask.redirect(flask.url_for("_result"))
        elif flask.request.method == "GET":
            return flask.render_template("quiz.html")

    @app.route("/result")
    def _result() -> str:
        return flask.render_template("result.html")

    @app.route("/edit", methods=["GET", "POST"])
    def _editprofile():
        return flask.render_template("editprofile.html")

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

    @app.route("/api/data")
    def _data() -> flask.Response:
        """Normal data."""
        return flask.jsonify({"x": 1})

    @app.route("/cooler_data")
    def _cooler() -> flask.Response:
        """Cooler data."""
        # also look into requests.Session
        # for bulk requests

        # make request
        resp = requests.get(api_url("data"))
        # parse response
        data = resp.json()
        cooler_data = {"y": data["x"] + 1}
        # return response
        return flask.jsonify(cooler_data)

    # Usernames mock
    known = {"alpha": 1, "beta": 2, "gamma": 3}

    @app.route("/api/usernames")
    def _usernames() -> flask.Response:
        """Query a list of usernames."""
        return flask.jsonify(list(known.keys()))

    @app.route("/api/usernames/<username>")
    def _username(username: str) -> flask.Response:
        """Query a username."""
        try:
            return flask.jsonify({"id": known[username], "username": username})
        except KeyError:
            flask.abort(404)

    return app
