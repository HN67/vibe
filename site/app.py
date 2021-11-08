"""Main Flask application."""

import flask


def create_app() -> flask.Flask:
    """Create the Flask instance."""

    # __name__ is a python module-level constant
    # that lets flask locate the project in the file system
    app = flask.Flask(__name__)

    @app.route("/")
    def _index() -> str:
        return "<p>Hello world</p>"

    return app
