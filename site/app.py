"""Main Flask application."""

import typing as t

import flask
import requests
from requests.api import get, request

import api


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
            return flask.redirect(
                flask.url_for("_profile", username=flask.request.form["username"])
            )
        moods = getqualia("moods")
        colors = getqualia("colors")
        scents = getqualia("scents")
        tastes = getqualia("tastes")
        shapes = getqualia("shapes")
        media = getqualia("media_genres")
        music = getqualia("music_genres")
        return flask.render_template(
            "quiz.html",
            moods=moods,
            colors=colors,
            scents=scents,
            tastes=tastes,
            shapes=shapes,
            media=media,
            music=music,
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

    app = api.build_api(app, mock=True)

    return app
