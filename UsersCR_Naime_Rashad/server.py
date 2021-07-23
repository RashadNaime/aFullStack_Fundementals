from flask import Flask, render_template, request, redirect, session
from user import User
app = Flask(__name__)
app.secret_key = "keep it secret, keep it safe."

# what is the default request method when declaring a route?
# GET Request
#all render templates are to display the pages 
@app.route("/users")
def index():
    context = {"all_users": User.get_all()}
    
    return render_template("index.html", **context)


@app.route("/users/new")
def create_user():
    return render_template("createuser.html")


@app.route("/users/<int:user_id>")
def specific_user(user_id):
    dict = {"id" : user_id}
    return render_template("singleuser.html", user = User.get_one(dict))


#starting the action routes that will redirect to render template routes
@app.route("/users/create", methods=["POST"])
def retrieve_form():
    User.create(request.form)
    return redirect("/users")

#debug
if __name__ == "__main__":
    app.run(debug = True)
