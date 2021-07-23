#import the mysqlconnection, establishes connection to the database
from flask_app.config.mysqlconnection import connectToMySQL
import re                               #re is used for regular expressions in python
from flask import flash                 #Flash to display error messages from validation
from flask_app import app, DB, bcrypt   #import app, the databse, bcrypt
# which is made by invoking the function Bcrypt with our app as an argument
from flask_app.models import user

class Pet:
    #Setup the constructor, with all attributes that match the users table fields. 
    def __init__(self, data):
        self.id = data['id']
        #establishing absraction and a one to many relationship
        if data['user_id']:                                        #prevent an infinite loop if the user_id is in the database
            self.user = user.User.get_one({"id": data['user_id']}) #this the relationship of the tables through the foreign key
        self.animal = data['animal']
        self.cool = data['cool']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data): #create a row of data in the database 
        query = """
            INSERT INTO pets (user_id, animal ,cool)
            VALUES (%(user_id)s, %(animal)s, %(cool)s);
        """

        #set the result equal to the database function, pass the database name, query, and data to create new row
        result = connectToMySQL(DB).query_db(query, data)
        return result


    @classmethod
    def get_all(cls): #get all the data from entire table
        query = "SELECT * FROM pets"
        results = connectToMySQL(DB).query_db(query)
        print(results) #result is always a list of  dictionary

        #create list to store the all the rows from the database
        all_pets = [] 
        for row in results:
            all_pets.append(cls(row)) #append to a list of objects

        return all_pets    


    #every function except for get_all() requires a dictionary to be passed into its parameter for data
    @classmethod
    def get_one(cls, data):
        #We must pass a dictionary into the query_db(query, data)
        query = "SELECT * FROM pets WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query, data)

        #if the selection does not exist, return false 
        if len(result) < 1:
            return False
        else:
            return cls(result[0])


    @classmethod
    def get_by_animal(cls, data): #exactly like get one, except grab the data by a specific attribute
        query = "SELECT * FROM pets WHERE animal = %(animal)s;"
        result = connectToMySQL(DB).query_db(query, data)
        
        if len(result) < 1:
            return False
        else:
            return cls(result[0])   

    
    @classmethod
    def update(cls, data): #edit the the data within a row of the table within database
        query = "UPDATE pets SET animal = %(animal)s, cool = %(cool) WHERE id = %(id)s;"

        return connectToMySQL(DB).query_db(query, data)

        
    @classmethod
    def delete(cls, data): #delete from a specific row, set the id
        query = "DELETE FROM pets WHERE id = %(id)s;"

        return connectToMySQL(DB).query_db(query, data)
            

    @staticmethod
    def validate(form_data): #validation is the process of sanitizing the input from the user taken from the form
        is_valid = True 
        #set flag to true, and if any user errors are found, set flag to false 
        if len(form_data.animal) < 2:
            flash("Must enter a real animal you silly goose", "animal")
            is_valid = False

        if len(form_data.cool) < 1:
            flash("Must enter a real animal you silly goose", "cool")
            is_valid = False

        return is_valid    
    