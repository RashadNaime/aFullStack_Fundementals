from flask import Flask, render_template, redirect, request, session 
from flask_app import app
app = Flask(__name__)
app.secret_key = "shhhhhh"

# ...server.py

