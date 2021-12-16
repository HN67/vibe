"""API Endpoints."""

import dataclasses
import logging
import typing as t

import flask
import mariadb
import toml

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


@dataclasses.dataclass()
class Result:
    """Database result."""

    headers: t.Tuple[str, ...]
    rows: t.Sequence[t.Tuple[t.Any, ...]]

    auto: t.Optional[int] = None


class Database:
    """Manage a connection to the database."""

    def __init__(self, **params: t.Union[str, int]) -> None:
        """Initialize a Database model."""
        self.connection = mariadb.connect(**params)
        self.cursor = self.connection.cursor()

    def procedure(
        self, name: str, arguments: t.Optional[t.Tuple[t.Any, ...]] = None
    ) -> Result:
        """Call a stored procedure.

        Returns a single result set, exhausting the others if they exist.
        """
        # we want a single cursor
        # at some point self.cursor might become a getter
        cursor = self.cursor

        cursor.callproc(name, arguments)

        try:
            data: t.Sequence[t.Tuple[t.Any, ...]] = cursor.fetchall()
        except mariadb.ProgrammingError:
            data = []

        if cursor.description is not None:
            try:
                headers: t.Tuple[str, ...] = tuple(
                    column[0] for column in cursor.description
                )
            except mariadb.ProgrammingError:
                headers = tuple()
        else:
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


def api_url(name: str) -> str:
    """Construct an absolute API URL from a relative URL.

    For example, if the site is running on http localhost:5000,
    api_url(flask.request, 'moods/happy') == http://localhost:5000/api/moods/happy
    """
    return flask.request.host_url + "api/" + name


def build_api_mock(app: flask.Flask) -> flask.Flask:
    """Register various API endpoints on the provided Flask app.

    Returns the app (which has had more routes registered).
    """

    # Usernames mock
    known = {"alpha": 1, "beta": 2, "gamma": 3}
    someuser = {
        "id": 1,
        "birthday": "MM/DD/YYYY",
        "email": "alpha@gmail.com",
        "displayName": "a",
        "bio": "bla bla bla",
    }

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

    @app.route("/api/client/<clientId>")
    def _client(clientId: str) -> flask.Response:
        """Query a client."""
        try:
            return flask.jsonify(
                {
                    "id": id,
                    "birthday": someuser["birthday"],
                    "email": someuser["email"],
                    "displayName": someuser["displayName"],
                    "bio": someuser["bio"],
                }
            )
        except KeyError:
            flask.abort(404)

    someresult = {
        "client": 1,
        "number": 1,
        "mood": "Sad",
        "taste": "Sour",
        "scent": "Bitter",
        "color": "Gray",
        "shape": "Line",
        "media_genre": "Sad",
        "music_genre": "Sad pop",
    }

    @app.route("/api/clients/<clientId>/results/all")
    def _results(clientId: str) -> flask.Response:
        """Query a client."""
        try:
            return flask.jsonify([someresult, someresult])
        except KeyError:
            flask.abort(404)

    moods = [{"name": "Sad"}, {"name": "Happy"}, {"name": "Angry"}]
    colors = [{"name": "Red"}, {"name": "Blue"}, {"name": "Pink"}]
    shapes = [{"name": "Triangle"}, {"name": "Circle"}, {"name": "Line"}]
    tastes = [{"type": "Bitter"}, {"type": "Sweet"}, {"type": "Sour"}]
    scents = [{"name": "Floral"}, {"name": "Woody"}, {"name": "Fresh"}]
    media = [{"name": "Fiction"}, {"name": "Action"}, {"name": "Horror"}]
    music = [{"name": "Pop"}, {"name": "R & B"}, {"name": "Rap"}]

    @app.route("/api/moods/")
    def _moods() -> flask.Response:
        """Query a client."""
        try:
            return flask.jsonify(moods)
        except KeyError:
            flask.abort(404)

    @app.route("/api/colors/")
    def _colors() -> flask.Response:
        """Query a client."""
        try:
            return flask.jsonify(colors)
        except KeyError:
            flask.abort(404)

    @app.route("/api/shapes/")
    def _shapes() -> flask.Response:
        """Query a client."""
        try:
            return flask.jsonify(shapes)
        except KeyError:
            flask.abort(404)

    @app.route("/api/scents/")
    def _scents() -> flask.Response:
        """Query a client."""
        try:
            return flask.jsonify(scents)
        except KeyError:
            flask.abort(404)

    @app.route("/api/tastes/")
    def _tastes() -> flask.Response:
        """Query a client."""
        try:
            return flask.jsonify(tastes)
        except KeyError:
            flask.abort(404)

    @app.route("/api/media_genres/")
    def _media() -> flask.Response:
        """Query a client."""
        try:
            return flask.jsonify(media)
        except KeyError:
            flask.abort(404)

    @app.route("/api/music_genres/")
    def _music() -> flask.Response:
        """Query a client."""
        try:
            return flask.jsonify(music)
        except KeyError:
            flask.abort(404)

    return app


def build_api(app: flask.Flask, mock: bool = False) -> flask.Flask:
    """Register various API endpoints on the provided Flask app.

    Returns the app (which has had more routes registered).
    """

    if mock:
        return build_api_mock(app)

    @app.get("/api/moods/")
    def _get_moods() -> flask.Response:
        """Query list of moods."""
        return flask.jsonify([mood for (mood,) in get_db().procedure("get_moods").rows])

    @app.get("/api/moods/<name>")
    def _get_mood(name: str) -> flask.Response:
        """Query a mood."""
        result = get_db().procedure("get_mood", (name,))
        try:
            out_name = result.rows[0][0]
        except IndexError:
            flask.abort(404)
        return flask.jsonify({"name": out_name})

    @app.put("/api/moods/<name>")
    def _put_mood(name: str) -> flask.Response:
        """Put a mood."""
        get_db().procedure("put_mood", (name,))
        return flask.jsonify({"name": name})

    @app.delete("/api/moods/<name>")
    def _delete_mood(name: str) -> flask.Response:
        """Delete a mood."""
        get_db().procedure("delete_mood", (name,))
        return flask.jsonify({"name": name})

    return app
