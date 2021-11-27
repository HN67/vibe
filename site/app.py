"""Main Flask application."""

import random
import typing as t

import flask


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

    return app
