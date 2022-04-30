#!/usr/bin/env python3
"""Credentials Distributor"""
from typing import List

from random import choice

from flask import Flask
from flask import request, send_from_directory, abort

from config import version, debug
from config import host, port
from service import get_groups, get_available_users, assign_user

__version__ = version

app = Flask("Accounts")

# Errors
@app.errorhandler(404)
def mistake404(code):
    return "Sorry, this page does not exist.", 405


@app.errorhandler(405)
def mistake405(code):
    return "The given call is not allowed by the application.", 405


@app.errorhandler(422)
def mistake422(code):
    return (
        "The request was well-formed but was unable to be followed due to semantic errors.",
        405,
    )


@app.errorhandler(500)
def mistake500(code):
    return "Server experienced internal problem.", 405


@app.errorhandler(504)
def mistake504(code):
    return "Unable to access internal service.", 405


@app.route("/group", methods=["GET"])
def groups():
    return {"result": [{"id": g.id, "desc": g.description} for g in get_groups()]}


@app.route("/group/<int:group_id>", methods=["GET", "POST"])
def users(group_id: int):
    """return list of users for the given group"""
    email = request.get_json(force=True)["text"]
    return {"result": get_available_users(group_id, email)}


# @app.get("/group/{group_id}/user")
# def random_user(group_id: int):
#     chosen = choice(users(group_id)["result"])
#     return register(group_id, chosen.id)


@app.route("/group/<int:group_id>/user/<int:user_id>", methods=["POST"])
def register(group_id: int, user_id: int):
    """mark user as taken and return password"""
    email = request.get_json(force=True)["text"]
    u = assign_user(group_id, user_id, email)
    if not u:
        abort(404, "Item not found")
    # return {"name": u.name, "password": u.password}
    return u


@app.route("/group/<int:group_id>/user", methods=["POST"])
def lucky(group_id: int):
    """assign random user"""
    email = request.get_json(force=True)["text"]
    us = [u["id"] for u in users(group_id)["result"] if u["available"]]
    return register(group_id, choice(us), email)


@app.route("/")
@app.route("/<string:filename>")
def static_files(filename="index.html"):
    return send_from_directory("static", filename)

application = app
if __name__ == "__main__":
    app.run(host, port, debug)
