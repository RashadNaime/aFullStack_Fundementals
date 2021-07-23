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


@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    dict={"id": user_id}
    return render_template("edituser.html", user = User.get_one(dict))


#starting the action routes that will redirect to render template routes
@app.route("/users/create", methods=["POST"])
def retrieve_form():
    final_result = User.create(request.form)
    return redirect(f"/users/{final_result}")

#update a single user 
@app.route("/users/<int:user_id>/edit/existing" , methods=["POST"])
def update_user(user_id):
    new_dict = {
        **request.form,
        "id": user_id
    }
    User.update(new_dict)
    return redirect("/users")


@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    User.delete({"id": user_id})
    return redirect("/users")


"""
This is for the routes for collar from morning lecture 
@app.route('/collars/new')
def new_collar_form():
    return render_template('new_collar.html')

@app.route('/collars/create', methods=['POST'])
def create_collar():
    Collar.create(request.form)
    return redirect ('/')


"""




#debug
if __name__ == "__main__":
    app.run(debug = True)
