"""Main Flask application."""

import random
import typing as t

import flask
import requests
from requests.api import get, request

# def get_data(name: t.Optional[str]) -> t.Mapping[str, int]:
#     """Obtain data from *somewhere*."""
#     if name:
#         return {f"{name}_x": random.randint(1, 4), f"{name}_y": random.randint(1, 4)}
#     else:
#         return {"x": random.randint(1, 4), "y": random.randint(1, 4)}


def getuserinfo(username):
    p = "usernames/" + username
    resp = requests.get(api_url(p))
    # parse response
    user = resp.json()
    p = "client/" + str(user["id"])
    resp = requests.get(api_url(p))
    userinfo = resp.json()
    return userinfo


def getuserresults(id):
    p = "clients/" + id + "/results/all"
    resp = requests.get(api_url(p))
    # parse response
    results = resp.json()
    return results


def getqualia(q):
    resp = requests.get(api_url(q))
    # parse response
    moods = resp.json()
    return moods


def currentinfo(s, userinfo):
    if flask.request.form[s] != "":
        return flask.request.form[s]
    else:
        return userinfo["bio"]


def api_url(name: str) -> str:
    """Construct an absolute API URL from a relative URL.

    For example, if the site is running on http localhost:5000,
    api_url(flask.request, 'moods/happy') == http://localhost:5000/api/moods/happy
    """
    return flask.request.host_url + "api/" + name


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

    @app.route("/profile/<username>")
    def _profile(username) -> str:
        userinfo = getuserinfo(username)
        results = getuserresults(userinfo["id"])
        print(results)
        return flask.render_template(
            "profile.html", username=username, userinfo=userinfo, results=results
        )

    @app.route("/login", methods=["GET", "POST"])
    def _login():
        error = None
        if flask.request.method == "POST":
            return flask.redirect(
                flask.url_for("_profile", username=flask.request.form["username"])
            )
        return flask.render_template("login.html", error=error)

    @app.route("/quiz", methods=["GET", "POST"])
    def _quiz() -> str:
        if flask.request.method == "POST":
            ## --- based on user input and connections from database creates the client's result and put it in the database
            print("hemlo")
            # make a result to fill in
            client_result = {
                "mood": "",
                "taste": "",
                "scent": "",
                "color": "",
                "shape": "",
                "media_genre": "",
                "music_genre": "",
            }
            print("hemlo1")
            username = flask.request.form["username"]
            print(username)
            print("hemlo2")
            # get their mood
            try:
                selected_mood = flask.request.form["mood"]
            # if they didn't cooperate just send them back to their profile like a loser
            except:
                return flask.redirect(
                    flask.url_for("_profile", username=flask.request.form["username"])
                )
            # if they did cooperate then update their result
            client_result["mood"] = selected_mood

            print("mood: " + client_result["mood"])

            # use result to fill in anything missing
            for q in ["color", "scent", "taste", "shape", "media_genre", "music_genre"]:
                # get value from the radio buttons
                selected = flask.request.form[q]
                # if they didn't pick anything then we give them a suggestions
                print(q + "  " + selected)
                if selected == "":
                    selected = "just vibe bro"
                #     qualia_connections_raw = requests.get(
                #         api_url(q + "_connections"), params={"mood": selected_mood}
                #     )
                #     qualia_connections = qualia_connections_raw.json()
                #     print(qualia_connections[0][q])
                #     selected = qualia_connections[0][q]
                # then add it to their result
                client_result[q] = selected
                print(q + "  " + selected)

            # now we put the result in the database for the client using the API
            username = flask.request.form["username"]
            userinfo = getuserinfo(username)
            requests.post(
                api_url("client/" + str(userinfo["id"] + "/results/")),
                params=client_result,
            )
            ## --- end

            return flask.redirect(flask.url_for("_profile", username=username))

        moods = getqualia("moods")
        colors = getqualia("colors")
        scents = getqualia("scents")
        tastes = getqualia("tastes")
        shapes = getqualia("shapes")
        media_genres = getqualia("media_genres")
        music_genres = getqualia("music_genres")
        return flask.render_template(
            "quiz.html",
            moods=moods,
            colors=colors,
            scents=scents,
            tastes=tastes,
            shapes=shapes,
            media_genres=media_genres,
            music_genres=music_genres,
        )

    @app.route("/<username>/edit", methods=["GET", "POST"])
    def _editprofile(username):
        userinfo = getuserinfo(username)
        if flask.request.method == "POST":
            bio = currentinfo("bio", userinfo)
            displayname = currentinfo("name", userinfo)

            email = currentinfo("email", userinfo)
            birthday = currentinfo("birthday", userinfo)
            data = {
                "birthday": birthday,
                "email": email,
                "displayName": displayname,
                "bio": bio,
            }
            # requests.post(
            #     api_url("client/" + str(userinfo["id"])), data=flask.jasonify(data)
            # )
            return flask.redirect(flask.url_for("_profile", username=username))
        return flask.render_template(
            "editprofile.html", username=username, userinfo=userinfo
        )

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

    @app.route("/api/client/<id>")
    def _client(id: str) -> flask.Response:
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

    @app.route("/api/clients/<id>/results/all")
    def _results(id: str) -> flask.Response:
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
    media_genres = [{"name": "Fiction"}, {"name": "Action"}, {"name": "Horror"}]
    music_genres = [{"name": "Pop"}, {"name": "R & B"}, {"name": "Rap"}]

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
    def _media_genres() -> flask.Response:
        """Query a client."""
        try:
            return flask.jsonify(media_genres)
        except KeyError:
            flask.abort(404)

    @app.route("/api/music_genres/")
    def _music_genres() -> flask.Response:
        """Query a client."""
        try:
            return flask.jsonify(music_genres)
        except KeyError:
            flask.abort(404)

    return app
