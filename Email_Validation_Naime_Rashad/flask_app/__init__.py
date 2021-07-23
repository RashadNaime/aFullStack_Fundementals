from flask import Flask

app = Flask(__name__)    # Create a new instance of the Flask class called "app"
app.secret_key = "if you have to ask, you'll never know"

