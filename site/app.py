"""Main Flask application."""

import logging
import typing as t

import flask
import requests
from requests.api import get, request

import api

root_logger = logging.getLogger()

FORMAT_STRING = "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s"
LOGGING_LEVEL = logging.DEBUG

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(FORMAT_STRING))
root_logger.addHandler(handler)
root_logger.setLevel(LOGGING_LEVEL)

# Remove werkzeug handlers
werkzeug_logger = logging.getLogger("werkzeug")
for _handler in list(werkzeug_logger.handlers):
    werkzeug_logger.removeHandler(_handler)


def getuserinfo(username):
    p = "usernames/" + username
    resp = requests.get(api.api_url(p))
    # parse response
    user = resp.json()
    p = "client/" + str(user["id"])
    resp = requests.get(api.api_url(p))
    userinfo = resp.json()
    return userinfo


def getuserresults(id):
    p = "clients/" + id + "/results/all"
    resp = requests.get(api.api_url(p))
    # parse response
    results = resp.json()
    return results


def getqualia(q):
    resp = requests.get(api.api_url(q))
    # parse response
    moods = resp.json()
    return moods


def currentinfo(s, userinfo):
    if flask.request.form[s] != "":
        return flask.request.form[s]
    else:
        return userinfo["bio"]


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
            #     api.api_url("client/" + str(userinfo["id"])), data=flask.jasonify(data)
            # )
            return flask.redirect(flask.url_for("_profile", username=username))
        return flask.render_template(
            "editprofile.html", username=username, userinfo=userinfo
        )

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

    app = api.build_api(app, mock=False)

    return app
