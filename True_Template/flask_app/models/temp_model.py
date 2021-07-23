#import the mysqlconnection, establishes connection to the database
from flask_app.config.mysqlconnection import connectToMySQL
import re                               #re is used for regular expressions in python
from flask import flash                 #Flash to display error messages from validation
from flask_app import app, DB, bcrypt   #import app, the databse, bcrypt

#connect the other model into the file, but do not call it by its class, call the file name, then call the class using the file name
from flask_app.models import user


class Temp:
    #Setup the constructor, with all attributes that match the users table fields. 
    def __init__(self, data):
        self.id = data['id']
        #establishing absraction and a one to many relationship
        if data['user_id']:                                        #prevent an infinite loop if the user_id is in the database
            self.user = user.User.get_one({"id": data['user_id']}) #this the relationship of the tables through the foreign key

        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data): #create a row of data in the database 
        query = """
            INSERT INTO table_name (table_fields1, table_fields2 ,table_fields3)
            VALUES (%(table_fields1)s, %(table_fields2)s, %(table_fields3)s);
        """

        #set the result equal to the database function, pass the database name, query, and data to create new row
        result = connectToMySQL(DB).query_db(query, data)
        return result


    @classmethod
    def get_all(cls): #get all the data from entire table
        query = "SELECT * FROM table_name"
        results = connectToMySQL(DB).query_db(query)
        print(results) #result is always a list of  dictionary

        #create list to store the all the rows from the database
        all_table = [] 
        for row in results:
            all_table.append(cls(row)) #append to a list of objects

        return all_table    


    #every function except for get_all() requires a dictionary to be passed into its parameter for data
    @classmethod
    def get_one(cls, data):
        #We must pass a dictionary into the query_db(query, data)
        query = "SELECT * FROM table_name WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query, data)

        #if the selection does not exist, return false 
        if len(result) < 1:
            return False
        else:
            return cls(result[0])


    @classmethod
    def get_by_email(cls, data): #exactly like get one, except grab the data by a specific attribute
        query = "SELECT * FROM table_name WHERE table_field = %(table_field)s;"
        result = connectToMySQL(DB).query_db(query, data)
        
        if len(result) < 1:
            return False
        else:
            return cls(result[0])   

    
    @classmethod
    def update(cls, data): #edit the the data within a row of the table within database
        query = "UPDATE table_name SET table_fields = %(table_fields)s WHERE id = %(id)s;"

        return connectToMySQL(DB).query_db(query, data)

        
    @classmethod
    def delete(cls, data): #delete from a specific row, set the id
        query = "DELETE FROM table_name WHERE id = %(id)s;"

        return connectToMySQL(DB).query_db(query, data)
            

    @staticmethod
    def validate(form_data): #validation is the process of sanitizing the input from the user taken from the form
        is_valid = True 
        #set flag to true, and if any user errors are found, set flag to false 
        if len(form_data.fieldname) < 1:
            pass

        return is_valid    
    