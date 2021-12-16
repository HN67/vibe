"""API Endpoints."""

import dataclasses
import typing as t

import flask
import mariadb
import toml


@dataclasses.dataclass()
class Result:
    """Database result."""

    headers: tuple[str, ...]
    rows: t.Sequence[tuple[t.Any, ...]]

    auto: t.Optional[int] = None


class Database:
    """Manage a connection to the database."""

    def __init__(self, **params: t.Union[str, int]) -> None:
        """Initialize a Database model."""
        self.connection = mariadb.connect(**params)
        self.cursor = self.connection.cursor()

    def procedure(
        self, name: str, arguments: t.Optional[tuple[t.Any, ...]] = None
    ) -> Result:
        """Call a stored procedure.

        Returns a single result set, exhausting the others if they exist.
        """
        # we want a single cursor
        # at some point self.cursor might become a getter
        cursor = self.cursor

        cursor.callproc(name, arguments)

        try:
            data: t.Sequence[tuple[t.Any, ...]] = cursor.fetchall()
        except mariadb.ProgrammingError:
            data = []

        try:
            headers: tuple[str, ...] = tuple(column[0] for column in cursor.description)
        except mariadb.ProgrammingError:
            headers = tuple()

        auto: t.Optional[int] = cursor.lastrowid

        # documentation sucks real bad about mariadb
        # but it seems like this will return None if the results have been exhausted
        # nextset throws exception if non querying statement, e.g. INSERT
        try:
            while cursor.nextset():
                pass
        except mariadb.ProgrammingError:
            pass

        return Result(headers=headers, rows=data, auto=auto)


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
        return flask.jsonify([mood for (mood,) in get_db().procedure("get_moods").rows])

    return app
