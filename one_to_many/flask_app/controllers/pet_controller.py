from flask import Flask, render_template, redirect, request, session, flash # Import Flask to allow us to create our app
from flask_app.models.user import User #always import the classes from the model
from flask_app.models.pet import Pet
from flask_app.controllers import user_controller
from flask_app import app, bcrypt


@app.route("/create/pet")
def create_pet_form():
    if "unique_userid" not in session:
        return redirect("/")    
    
    return render_template("createpet.html")

@app.route("/process/new/pet", methods=['POST'])
def create_pet():

    new_pet = {
        **request.form, 
        "user_id": session["unique_userid"]
    }
    Pet.create(new_pet)
    return redirect("/users/page")

@app.route("/display/user/pets")
def display_user_pet():
    if "unique_userid" not in session:
        return redirect("/")       
    dict = {
        "id": session['unique_userid']
    } 
    print(session['unique_userid'])
    return render_template("userpet.html", user_pets = User.get_one_join(dict), logged_user = User.get_one(dict))



@app.route("/edit/pet/form/<int:pet_id>")
def display_edit_pet(pet_id):
    dict = {
        "id": pet_id
    }
    render_template("editpet.html", pet = Pet.get_one)
