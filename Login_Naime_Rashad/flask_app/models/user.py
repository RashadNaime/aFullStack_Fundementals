from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from flask_app import app, DB, bcrypt       
# which is made by invoking the function Bcrypt with our app as an argument



class User:
    schema = "user_login_schema"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.password = data['password']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """

        result = connectToMySQL(cls.schema).query_db(query, data)
        return result


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL(cls.schema).query_db(query)
        print(results) #result is always a list of  dictionary
        all_users = []
        for row in results:
            all_users.append(cls(row))
        return all_users      

    #every function except for get_all() requires a dictionary
    @classmethod
    def get_one(cls, data):
        #We must pass a dictionary into the query_db(query, data)
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.schema).query_db(query, data)

        if len(result) == 1:
            return cls(result[0])
        else:
            return False

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.schema).query_db(query, data)
        
        if len(result) == 1:
            return cls(result[0])
        else:
            return False    

    
    @classmethod
    def update(cls, data):
        pass

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.schema).query_db(query, data)
            
    @staticmethod
    def validate_registration(form_data):
        #set flag to true, and if any user errors are found, set flag to false 
        is_valid = True 
        #use regular expression for email, validate if the user inputted a correct email, and if email is within the database
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        if not EMAIL_REGEX.match(form_data['email']):
            flash("Invalid email format")
            is_valid = False 
        elif User.get_by_email({"email": form_data['email']}):
            flash("The Email Already Exists")
            is_valid = False     

        #validate the first and last names are inputted correctly
        if len(form_data['first_name']) < 3:
            flash("Please enter a proper first name")
        if len(form_data['last_name']) < 3:
            flash("Please enter a proper last name")

        #validate the password, make sure its length is at least 8 characters and the confirmation password is the same
        if len(form_data['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        elif form_data['password'] != form_data['confirm']:
            flash("Password and Confirm Password must match")
            is_valid = False

        return is_valid    
    

    @staticmethod
    def validate_login(form_data):
        #create an instance of the user class, but compare the email from the form data
        user = User.get_by_email({"email":form_data['email']})

        #use if statemtents to check if the emails match and if the password is correct
        if not user:
            flash("User Email does not exist, please try another, or register for an account")
            return False

        if not bcrypt.check_password_hash(user.password, form_data['password']):
            flash("Password was incorrect, please re-enter the proper password")
            return False
        
        return True
