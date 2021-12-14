"""API Endpoints."""

import typing as t

import flask
import mariadb
import toml


class Database:
    """Manage a connection to the database."""

    def __init__(self, **params: t.Union[str, int]) -> None:
        """Initialize a Database model."""
        self.connection = mariadb.connect(**params)
        self.cursor = self.connection.cursor()

    def execute(
        self, query: str, arguments: t.Optional[t.Tuple[t.Any, ...]] = None
    ) -> t.Iterable[t.Tuple[t.Any, ...]]:
        """Execute a query on the database."""
        self.cursor.execute(query, arguments)
        yield from self.cursor


CONFIG = "config.toml"


def get_db() -> Database:
    """Provide a Database.

    May be reused.
    """
    config = toml.load(CONFIG)
    database = Database(**config["database"])
    return database


def build_api(app: flask.Flask) -> flask.Flask:
    """Register various API endpoints on the provided Flask app.

    Returns the app (which has had more routes registered).
    """

    @app.get("/api/moods/")
    def _moods() -> flask.Response:
        """Query list of moods."""
        return flask.jsonify(
            [mood for (mood,) in get_db().execute("CALL get_moods();")]
        )

    return app
