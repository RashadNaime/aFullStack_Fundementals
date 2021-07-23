from flask import Flask, render_template, request, redirect, session
from dojo import Dojo
app = Flask(__name__)
app.secret_key = "keep it secret, keep it safe."

# what is the default request method when declaring a route?
# GET Request
@app.route("/")
def index():
    return render_template("index.html")


# we need to specify that this route is for a post request
@app.route("/process", methods = ["POST"])
def create_user():
    print(request.form) 
    # request.form is a dictionary
    # keys and values
    # session is dictionary
    if not Dojo.validate(request.form):
        return redirect("/")
    
    last_id = Dojo.create(request.form)
    return redirect(f"/results/{last_id}")
    

    return redirect("/results") # redirect makes a new GET request to a different route

@app.route('/results/<int:id>')
def display_result(id):
    dict = {"id": id}
    return render_template("results.html", dojo_id = Dojo.get_one(dict))

# @app.route("/display")
# def display():
#     # print("SUCCESSFUL REDIRECT")
#     print(session['name'])
#     return render_template(
#         "display.html",
#         name = session['name'],
#         age = session['age'],
#         hair_color = session['hair_color']
#     )



if __name__ == "__main__":
    app.run(debug = True)