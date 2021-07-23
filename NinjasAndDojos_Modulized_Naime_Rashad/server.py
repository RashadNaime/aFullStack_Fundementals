from flask_app import app
from flask_app.controllers import ninja_controller, dojo_controller


#debug
if __name__ == "__main__":
    app.run(debug = True)