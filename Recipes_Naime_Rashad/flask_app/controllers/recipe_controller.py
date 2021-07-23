from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.recipe import Recipe
from flask_app import app, bcrypt
from flask_app.controllers import user_controller
from flask_app.models.user import User

@app.route("/new/recipe/form")
def new_recipe_form():
    if not "unique_userid" in session:
        return redirect("/")

    dict = {"id": session["unique_userid"]}

    #pass the entire table, and pass in the current logged in user
    return render_template("create_recipe.html", logged_user = User.get_one(dict))


@app.route("/new/recipe/create", methods=["POST"])
def create_recipe():
    print(request.form)
    if not Recipe.validate_recipe(request.form):
        return redirect("/new/recipe/form")
    print("PLEEEEEEEEEEAAASSSSS", request.form["under_30_minutes"])
    
    form_data = { **request.form, "user_id": session['unique_userid']} # This is how to insert user id into creating something 

    Recipe.create(form_data)

    return redirect("/users/page")


@app.route("/edit/recipe/form/<int:recipe_id>")
def edit_recipe_form(recipe_id):
    if not "unique_userid" in session:
        return redirect("/")

    dict = {"id": session["unique_userid"]}
    dict_recipe = {"id": recipe_id}
    logged_user = User.get_one(dict)
    recipe = Recipe.get_one(dict_recipe)

    if logged_user.id != recipe.user.id:
        flash("Stop trying to break my website")
        return redirect('/users/page')
        
    #pass the entire table, and pass in the current logged in user
    return render_template("edit_recipe.html", logged_user = logged_user, recipe = recipe)   


@app.route("/existing/recipe/edit/<int:recipe_id>", methods=["POST"])
def edit_recipe(recipe_id):
    if not Recipe.validate_recipe(request.form):
        return redirect(f"/edit/recipe/form/{recipe_id}")
    
    form_data = { **request.form, "user_id": session['unique_userid'], "id": recipe_id} # This is how to insert user id into creating something 

    Recipe.update(form_data)

    return redirect("/users/page")


@app.route("/recipe/<int:id>/view")
def display_recipe(id):
    dict = {"id": id}
    user_dict = {"id": session['unique_userid']}
    return render_template("view_recipe.html", logged_user = User.get_one(user_dict), recipe = Recipe.get_one(dict))

@app.route("/delete/recipe/<int:recipe_id>")
def delete_recipe(recipe_id):
    dict = {"id": recipe_id}
    Recipe.delete(dict)

    return redirect("/users/page")   


