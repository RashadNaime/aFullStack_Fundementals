from flask import Flask, render_template, redirect, session, request
from flask_app import app
from flask_app.models.ninja import Ninja
from flask_app.models.dojo import Dojo
#from flask_app.models.user import User

# what is the default request method when declaring a route?
# GET Request
#all render templates are to display the pages 
@app.route("/dojos")
def index_dojo():
    context = {"all_dojos": Dojo.get_all()}
    return render_template("index.html", **context)


@app.route("/dojos/<int:dojo_id>")
def display_ninjas_info(dojo_id):
    dict = {"id": dojo_id}
    return render_template("displayninjas.html", dojo = Dojo.get_one(dict))





#taking input from the form on index.html to make a new dojo
@app.route("/dojos/create", methods=["POST"])
def new_dojo():
    Dojo.create(request.form)
    return redirect("/dojos")