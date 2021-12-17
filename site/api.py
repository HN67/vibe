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

    def vertical(self, column: int = 0) -> t.Sequence[t.Any]:
        """Return a vertical column extracted from this Result rows."""
        return [row[column] for row in self.rows]

    @staticmethod
    def weave(
        headers: t.Tuple[str, ...], row: t.Tuple[t.Any, ...]
    ) -> t.Mapping[str, t.Any]:
        """Weave a headers tuple with a row to produce a mapping.

        Although headers and row should be the same size,
        if they are not the longer is truncated.
        """
        return dict(zip(headers, row))

    def one(self, index: int = 0) -> t.Optional[t.Mapping[str, t.Any]]:
        """Return a single result, woven."""
        try:
            return self.weave(self.headers, self.rows[index])
        except IndexError:
            return None

    def all(self) -> t.Sequence[t.Mapping[str, t.Any]]:
        """Return the results woven."""
        return [self.weave(self.headers, row) for row in self.rows]


class Database:
    """Manage a connection to the database."""

    def __init__(self, **params: t.Union[str, int]) -> None:
        """Initialize a Database model."""
        self.connection = mariadb.connect(**params)

    def procedure(
        self, name: str, arguments: t.Optional[t.Tuple[t.Any, ...]] = None
    ) -> Result:
        """Call a stored procedure.

        Returns a single result set, exhausting the others if they exist.
        """
        logger.info("Performing procedure %s with arguments %s", name, arguments)

        # Create a new cursor, helps ensure not deadlocking
        connection = self.connection
        with connection.cursor() as cursor:

            cursor.callproc(name, arguments)

            try:
                data: t.Sequence[t.Tuple[t.Any, ...]] = cursor.fetchall()
            except mariadb.ProgrammingError as e:
                logger.debug("Exception getting data from cursor: %s", e)
                data = []

            if cursor.description is not None:
                try:
                    headers: t.Tuple[str, ...] = tuple(
                        column[0] for column in cursor.description
                    )
                except mariadb.ProgrammingError as e:
                    logger.debug("Exception getting headers: %s", e)
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
            except mariadb.ProgrammingError as e:
                logger.debug("Exception advancing result sets: %s", e)

            # try committing?
            connection.commit()

            return Result(headers=headers, rows=data, auto=auto)

    def close(self) -> None:
        """Close the database connection."""
        self.connection.close()

    def __enter__(self) -> "Database":
        """Return a Context Manager of this connection."""
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        """Close this connection."""
        self.close()


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
                    "id": clientId,
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

    tc = [{"taste": "bitter", "mood": "sad"}, {"taste": "sweet", "mood": "happy"}]
    cc = [
        {"color": "red", "mood": "sad"},
    ]
    shapec = [
        {"shape": "circle", "mood": "sad"},
    ]
    scentc = [
        {"scent": "woody", "mood": "sad"},
    ]
    musicc = [
        {"music": "R & B", "mood": "sad"},
    ]
    mediac = [
        {"media": "fiction", "mood": "sad"},
    ]

    @app.route("/api/<q>_connections/")
    def _connection(q) -> flask.Response:
        """Query a client."""
        try:
            mood = flask.request.args.get("mood")
            print("mood is: " + mood)
            result = []
            if q == "tastes":
                for con in tc:
                    if con["mood"] == mood:
                        result.append(con)
            elif q == "colors":
                for con in cc:
                    if con["mood"] == mood:
                        result.append(con)
            elif q == "scents":
                for con in scentc:
                    if con["mood"] == mood:
                        result.append(con)
            elif q == "shapes":
                for con in shapec:
                    if con["mood"] == mood:
                        result.append(con)
            elif q == "music_genres":
                for con in musicc:
                    if con["mood"] == mood:
                        result.append(con)
            else:
                for con in mediac:
                    if con["mood"] == mood:
                        result.append(con)
            return flask.jsonify(result)
        except KeyError:
            flask.abort(404)

    return app


@dataclasses.dataclass()
class Resource:
    """Denote name and structure of a resource."""

    name: str
    attrs: t.Sequence[str]

    @property
    def others(self) -> t.Sequence[str]:
        """Everything except first attr."""
        return self.attrs[1:]

    @property
    def key(self) -> str:
        """First attr."""
        return self.attrs[0]


def build_resource_api(
    resource: Resource, alt: t.Optional[str] = None
) -> flask.Blueprint:
    """Automatically build and register endpoints for a resource on a bluepint.

    Assumes the existence of certain stored procedures.
    """

    if alt is None:
        alt = resource.name

    path = f"/api/{resource.name}s"
    specific_path = "/<key>"

    bp = flask.Blueprint(f"{resource.name}s", __name__, url_prefix=path)

    @bp.get("/")
    def _get_keys() -> flask.Response:
        """Query list of resources."""
        with get_db() as db:
            # return flask.jsonify([mood for (mood,) in db.procedure("get_moods").rows])
            return flask.jsonify(db.procedure(f"get_{alt}s").vertical())

    @bp.get(specific_path)
    def _get(key: str) -> flask.Response:
        """Query a resource."""
        with get_db() as db:
            result = db.procedure(f"get_{alt}", (key,))
            try:
                return flask.jsonify(result.one())
            except IndexError:
                flask.abort(404)

    @bp.put(specific_path)
    def _put(key: str) -> flask.Response:
        """Put a resource."""
        body = flask.request.json
        if body is None:
            flask.abort(400)
        parameters = (
            tuple([key] + [body[attr] for attr in resource.others])
            if resource.others
            else None
        )
        with get_db() as db:
            db.procedure(f"put_{alt}", parameters)
        return flask.jsonify({resource.key: key})

    @bp.delete(specific_path)
    def _delete(key: str) -> flask.Response:
        """Delete a resource."""
        with get_db() as db:
            db.procedure(f"delete_{alt}", (key,))
        return flask.jsonify({resource.key: key})

    return bp


def build_connections_api(
    resource: Resource,
    other: Resource,
    alt: t.Optional[str] = None,
) -> flask.Blueprint:
    """Build a blueprint for a connections API between two resources."""

    if alt is None:
        alt = resource.name

    path = f"/api/{resource.name}s_connections"
    bp = flask.Blueprint(f"{resource.name}s_connections", __name__, url_prefix=path)

    @bp.get("/")
    def _connections() -> flask.Response:
        """Query connections."""
        local_value = flask.request.args.get(resource.name)
        other_value = flask.request.args.get(other.name)

        with get_db() as db:
            if local_value and other_value:
                result = db.procedure(
                    f"get_{alt}affects_{alt}_{other.name}", (local_value, other_value)
                )
            elif local_value:
                result = db.procedure(f"get_{alt}affects_{alt}", (local_value,))
            elif other_value:
                result = db.procedure(f"get_{alt}affects_{other.name}", (other_value,))
            else:
                result = db.procedure(f"get_{alt}affects")

        return flask.jsonify(result.all())

    @bp.post("/")
    def _post_connection() -> flask.Response:
        """Put a connection."""

        data = flask.request.json

        if data is None:
            flask.abort(400)

        local_value = data[resource.name]
        other_value = data[other.name]

        with get_db() as db:
            db.procedure(f"put_{alt}affects", (local_value, other_value))

        return flask.jsonify({resource.name: local_value, other.name: other_value})

    @bp.delete("/")
    def _delete_connection() -> flask.Response:
        """Delete a connection."""

        data = flask.request.json

        if data is None:
            flask.abort(400)

        local_value = data[resource.name]
        other_value = data[other.name]

        with get_db() as db:
            db.procedure(f"delete_{alt}affects", (local_value, other_value))

        return flask.jsonify({resource.name: local_value, other.name: other_value})

    return bp


def build_api(app: flask.Flask, mock: bool = False) -> flask.Flask:
    """Register various API endpoints on the provided Flask app.

    Returns the app (which has had more routes registered).
    """

    if mock:
        return build_api_mock(app)

    # TODO
    # Make result endpoints also modify Affects tables
    # Make connections endpoints and custom endpoints

    mood = Resource("mood", ["name"])

    simple_resources: t.List[t.Tuple[Resource, t.Optional[str]]] = [
        (Resource("taste", ["type"]), None),
        (Resource("scent", ["name", "family"]), None),
        (Resource("shape", ["name", "sides"]), None),
        (Resource("color", ["name", "hue", "saturation", "brightness"]), None),
    ]

    # neccesary for explicit typing
    mood_pair: t.List[t.Tuple[Resource, t.Optional[str]]] = [(mood, None)]

    resources: t.List[t.Tuple[Resource, t.Optional[str]]] = (
        mood_pair
        + simple_resources
        + [
            (Resource("music_genre", ["name"]), "musicgenre"),
            (Resource("media_genre", ["name"]), "mediagenre"),
            (Resource("admin", ["id", "permissions"]), None),
            (
                Resource("client", ["id", "birthday", "email", "displayName", "bio"]),
                None,
            ),
        ]
    )

    qualia: t.List[t.Tuple[Resource, t.Optional[str]]] = simple_resources + [
        (Resource("music_genre", ["name"]), "music"),
        (Resource("media_genre", ["name"]), "media"),
    ]

    for resource, alt in resources:
        app.register_blueprint(build_resource_api(resource, alt))

    for resource, alt in qualia:
        app.register_blueprint(build_connections_api(resource, mood, alt))

    return app
