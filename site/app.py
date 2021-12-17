"""Main Flask application."""

import logging
import typing as t

import flask
import requests
from requests.api import get, request

import api

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

root_logger = logging.getLogger()

FORMAT_STRING = "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s"
LOGGING_LEVEL = logging.INFO

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
    p = "clients/" + str(user["id"])
    resp = requests.get(api.api_url(p))
    userinfo = resp.json()
    return userinfo


def getuserresults(id):
    p = "clients/" + str(id) + "/results/all"
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
        return userinfo[s]


def getconnections(q, m):
    resp = requests.get(api.api_url(q + "_connections"), params={"mood": m})
    # parse response
    moods = resp.json()
    return moods


def makeconnection(q, m, s):
    requests.post(api.api_url(q + "_connections"), json={q: s, "mood": m})
    # parse response
    return


def newuser(username):
    requests.post(api.api_url("users/"), json={"username": username})
    newuser = requests.get(api.api_url("usernames/" + username)).json()
    # make a new, empty profile
    newuserdata = {
        "birthday": "YYYY/MM/DD",
        "email": "email",
        "displayName": "display name",
        "bio": "biography",
    }
    requests.put(api.api_url("clients/" + str(newuser["id"])), json=newuserdata)
    return


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
            username = flask.request.form["username"]

            # check if they are a new user. if they are, makes a new, empty profile
            response = requests.get(api.api_url("usernames/" + username))
            if not response.ok:
                newuser(username)

            return flask.redirect(flask.url_for("_profile", username=username))
        return flask.render_template("login.html", error=error)

    @app.route("/quiz", methods=["GET", "POST"])
    def _quiz() -> str:
        if flask.request.method == "POST":
            ## --- based on user input and connections from database creates the client's result and put it in the database
            # make a result to fill in
            client_result = {
                "mood": "",
                "taste": "",
                "scent": "",
                "color": "",
                "shape": "",
                "media": "",
                "music": "",
            }

            # get their mood
            try:
                selected_mood = flask.request.form["mood"]
            # if they didn't cooperate just send them back to the quiz like a loser
            except:
                return flask.redirect(flask.url_for("_quiz"))
            # if they did cooperate then update their result
            client_result["mood"] = selected_mood

            print("mood: " + client_result["mood"])

            # fill in the rest of the result
            for q in [
                "color",
                "scent",
                "taste",
                "shape",
                "media",
                "music",
            ]:
                # get value from the radio buttons
                selected = flask.request.form[q]
                # if they didn't pick anything then we give them a suggestions
                if selected == "":
                    qualia_connections = getconnections((q + "s"), selected_mood)
                    selected = qualia_connections[0][q]
                # if they did then we make a connection with that
                else:
                    makeconnection((q + "s"), selected_mood, selected)
                    print(
                        "made connection: ", q + ": " + selected, "  " + selected_mood
                    )
                # then add whatever it was to their result
                client_result[q] = selected

            # now we put the result in the database for the client using the API
            username = flask.request.form["username"]

            # check if they are a new user. if they are, makes a new, empty profile
            response = requests.get(api.api_url("usernames/" + username))
            if not response.ok:
                newuser(username)

            # now there is a user id to get B)
            userinfo = getuserinfo(username)

            print(client_result)
            requests.post(
                api.api_url("clients/" + str(userinfo["id"]) + "/results/"),
                json=client_result,
            )
            ## --- end

            return flask.redirect(flask.url_for("_profile", username=username))

        moods = getqualia("moods")
        colors = getqualia("colors")
        scents = getqualia("scents")
        tastes = getqualia("tastes")
        shapes = getqualia("shapes")
        medias = getqualia("medias")
        musics = getqualia("musics")
        return flask.render_template(
            "quiz.html",
            moods=moods,
            colors=colors,
            scents=scents,
            tastes=tastes,
            shapes=shapes,
            medias=medias,
            musics=musics,
        )

    @app.route("/<username>/edit", methods=["GET", "POST"])
    def _editprofile(username):
        userinfo = getuserinfo(username)
        if flask.request.method == "POST":
            bio = currentinfo("bio", userinfo)
            displayname = currentinfo("displayName", userinfo)

            email = currentinfo("email", userinfo)
            birthday = currentinfo("birthday", userinfo)
            data = {
                "birthday": birthday,
                "email": email,
                "displayName": displayname,
                "bio": bio,
            }
            logger.info("Sending data %s", data)
            requests.put(api.api_url("clients/" + str(userinfo["id"])), json=data)
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
