from flask import Flask, render_template, redirect, session, request
from flask_app import app
from flask_app.models.ninja import Ninja
from flask_app.models.dojo import Dojo
#from flask_app.models.user import User

# what is the default request method when declaring a route?
# GET Request
#all render templates are to display the pages 
@app.route("/ninja")
def start_ninja():
    context = {"all_dojos": Dojo.get_all()}
    return render_template("createninja.html", **context)

@app.route("/ninja/create", methods=["POST"])
def create_from_form():
    dojo_id = request.form["dojo_id"]
    Ninja.create(request.form)
    return redirect(f"/dojos/{dojo_id}")