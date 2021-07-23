#import the mysqlconnection, establishes connection to the database
from flask_app.config.mysqlconnection import connectToMySQL
import re                               #re is used for regular expressions in python
from flask import flash                 #Flash to display error messages from validation
from flask_app import app, DB, bcrypt   #import app, the databse, bcrypt
# which is made by invoking the function Bcrypt with our app as an argument


#create a class to access the database
class User:
    #Setup the constructor, with all attributes that match the users table fields. 
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.password = data['password']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.table_names = []

    @classmethod
    def create(cls, data): #create a row of data in the database 
        query = """
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """

        #set the result equal to the database function, pass the database name, query, and data to create new row
        result = connectToMySQL(DB).query_db(query, data)
        return result


    @classmethod
    def get_all(cls): #get all the data from entire table
        query = "SELECT * FROM users"
        results = connectToMySQL(DB).query_db(query)
        print(results) #result is always a list of  dictionary

        #create list to store the objects from the database
        all_users = [] 
        for row in results:
            all_users.append(cls(row)) #append to a list of objects

        return all_users     


    #every function except for get_all() requires a dictionary to be passed into its parameter for data
    @classmethod
    def get_one(cls, data):
        #We must pass a dictionary into the query_db(query, data)
        query = "SELECT * FROM users WHERE id = %(id)s;"

        '''
        THIS IS THE JOIN FOR A ONE TO MANY RELATIONSHIP

        query = "SELECT * FROM users LEFT JOIN table_name ON user.id = table_name.user_id WHERE user.id = %(id)s;
        results = connectToMySQL(DB).query_db(query, data)

        user = cls(results[0]) #hold the specfic user

        if results[0]['table_names.id'] != None:
            for row in results:
                row_data = {
                    **row, 
                    "id": row["table_names.id"],
                    "created_at": row["table_names.created_at"],
                    "updated_at": row["table_names.updated_at"],
                    "user_id" = False
                }
                user.table_names.append(table_model.Temp(row_data)) #append to the specific user list

        return user
        '''
        result = connectToMySQL(DB).query_db(query, data)

        #if the selection does not exist, return false 
        if len(result) < 1:
            return False
        else:
            return cls(result[0])


    @classmethod
    def get_by_email(cls, data): #exactly like get one, except grab the data by a specific attribute
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DB).query_db(query, data)
        
        if len(result) < 1:
            return False
        else:
            return cls(result[0])   

    
    @classmethod
    def update(cls, data): #edit the the data within a row of the table within database
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s;"

        return connectToMySQL(DB).query_db(query, data)

        
    @classmethod
    def delete(cls, data): #delete from a specific row, set the id
        query = "DELETE FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DB).query_db(query, data)
            
    @staticmethod
    def validate_registration(form_data): #validation is the process of sanitizing the input from the user taken from the form
        is_valid = True 
        #set flag to true, and if any user errors are found, set flag to false 

        #use regular expression for email, validate if the user inputted a correct email, and if email is within the database
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        if not EMAIL_REGEX.match(form_data['email']): #if the email is not formatted correctly
            flash("Invalid email format", "email")
            is_valid = False 
        elif User.get_by_email({"email": form_data['email']}): #if the email already exists within the database
            flash("The Email Already Exists", "email")
            is_valid = False     

        #validate the first and last names are inputted correctly
        if len(form_data['first_name']) < 3:
            flash("Please enter a proper first name", "first_name")
            is_valid = False

        if len(form_data['last_name']) < 3:
            flash("Please enter a proper last name", "last_name")
            is_valid = False

        #validate the password, make sure its length is at least 8 characters and the confirmation password is the same
        if len(form_data['password']) < 8:
            flash("Password must be at least 8 characters.", "password")
            is_valid = False
        elif form_data['password'] != form_data['confirm']:
            flash("Password and Confirm Password must match", "confirm_password")
            is_valid = False

        return is_valid    
    

    @staticmethod
    def validate_login(form_data): #validation from the login portion

        #create an instance of the user class, but compare the email from the form data
        user = User.get_by_email({"email":form_data['email']})

        #use if statements to check if the emails match and if the password is correct
        if not user:
            flash("User Email does not exist, please try another, or register for an account", "login_email")
            return False

        #use hash function to check the inputted password from login, to the database hashed password
        if not bcrypt.check_password_hash(user.password, form_data['password']):
            flash("Password was incorrect, please re-enter the proper password", "login_password")
            return False
        
        return True
