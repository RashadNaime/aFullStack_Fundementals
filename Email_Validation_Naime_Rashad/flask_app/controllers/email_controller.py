from flask import Flask, render_template, redirect, request # Import Flask to allow us to create our app
from flask_app import app

from flask_app.models.email import Email



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def get_form():
    if not Email.validate(request.form):
        return redirect("/")
    
    Email.create(request.form)
    return redirect(f"/success/{request.form['email']}")

@app.route("/success/<string:email>")
def display_success(email):
    dict = {"email": email}
    return render_template("success.html", email_list = Email.get_all(), new_email = Email.get_one(dict))

@app.route("/delete/email/<int:id>")
def delete_email(id):
    dict_delete = {"id": id}
    Email.delete(dict_delete)
    return render_template("success.html", email_list = Email.get_all())