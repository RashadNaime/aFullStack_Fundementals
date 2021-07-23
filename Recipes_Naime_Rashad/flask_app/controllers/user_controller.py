#importing flask, render_template to create pages, request to grab data from form, session to store session data, and flash to display errors
#and redirect to move to new route after taking in form data
from flask import Flask, render_template, redirect, request, session, flash # Import Flask to allow us to create our app
from flask_app.models.user import User #always import the classes from the model
from flask_app import app, bcrypt
from flask_app.models.recipe import Recipe

#index page, will start and display login and registration forms 
@app.route("/")
def index():
    # if there is a user in session, start on the user page
    if "unique_userid" in session:
        return redirect("/users/page")

    return render_template("index.html")


#taking the form data from the registration portion of the index page
@app.route("/register/validate", methods=["POST"])
def valid_register():
    #validate all the input and redirect back to index with error messages displaying
    if not User.validate_registration(request.form):
        return redirect("/")


    #get the hash for the password 
    new_hash = bcrypt.generate_password_hash(request.form['password'])
    #store all the data from the new request.form 
    new_dict = {
        **request.form,
        "password": new_hash
    }
    
    #create the new user, and store the id into new_user variable
    new_user = User.create(new_dict) #will return new id of user from database

    session["unique_userid"] = new_user #pass the id into session 

    return redirect("/users/page")


#This will validate and pass the form information for login
@app.route("/login/validate", methods=["POST"])
def valid_login():
    #validate all the input and redirect back to index with error messages displaying
    if not User.validate_login(request.form):
        flash("Cannot enter users page without logging in")
        return redirect("/")

    user = User.get_by_email({"email": request.form['email']}) #get the unique email, and store the id into session

    session["unique_userid"] = user.id

    return redirect("/users/page")


#this route displays the users page after login
@app.route('/users/page')
def user_page():
    #If the user is not in session, redirect back into login
    if "unique_userid" not in session:
        return redirect("/")
    
    #set the dictionary with the unique id of the user in session
    dict = {"id": session["unique_userid"]}

    #pass the entire table, and pass in the current logged in user
    return render_template("users.html",logged_user = User.get_one(dict), all_recipes = Recipe.get_all()) # logged_user = User.get_one_join(dict)
    # This displays all users AND displays the list of whatever the current user has created.


#logout button, will clear session and restart back to login page
@app.route("/user/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/update/<int:id>/likes")
def count(id):

    dict = {"id": id}
    newPet = Pet.get_one(dict)

    dict2 = {"id": id, 
    "animal": newPet.animal,
    "cool": newPet.cool,
    "count": newPet.count+1}

    Pet.update(dict2)

    return redirect("/users/page")

