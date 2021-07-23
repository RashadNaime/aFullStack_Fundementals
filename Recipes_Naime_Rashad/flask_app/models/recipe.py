from flask_app.config.mysqlconnection import connectToMySQL
import re                               
from flask import flash                 
from flask_app import app, DB, bcrypt  

from flask_app.models import user


class Recipe:
    def __init__(self, data):
        self.id = data['id']

        if data['user_id']: #set conditional, and establish one to many relationship with user                                        
            self.user = user.User.get_one({"id": data['user_id']})  
        self.name = data['name']
        self.description = data['description']
        self.under_min = data['under_30_minutes']
        self.instructions = data['instructions']
        self.count = data['count']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO recipes (user_id, name, description, under_30_minutes, instructions)
            VALUES (%(user_id)s, %(name)s, %(description)s, %(under_30_minutes)s, %(instructions)s);
        """

        result = connectToMySQL(DB).query_db(query, data)
        return result


    @classmethod
    def get_all(cls): #get all the data from entire table
        query = "SELECT * FROM recipes"
        results = connectToMySQL(DB).query_db(query)

        #create list to store the all the rows from the database
        all_recipes = [] 

        for row in results:
            all_recipes.append(cls(row)) #append to a list of objects

        return all_recipes   


    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query, data)

        #if the selection does not exist, return false 
        if len(result) < 1:
            return False
        else:
            return cls(result[0])


    @classmethod
    def update(cls, data): # Edit the the data within a row of the table within database
        if "count" in data: # This is checking for the count when we click on the like, if count is in the data.
            query = "UPDATE recipes SET count = %(count)s WHERE id = %(id)s;"
        else: query = """
            UPDATE recipes SET name = %(name)s, description = %(description)s, under_30_minutes = %(under_30_minutes)s, instructions = %(instructions)s
            WHERE id = %(id)s;
        """
        return connectToMySQL(DB).query_db(query, data)

        
    @classmethod
    def delete(cls, data): #delete from a specific row, set the id
        query = "DELETE FROM recipes WHERE id = %(id)s;"

        return connectToMySQL(DB).query_db(query, data)

    
    @staticmethod
    def validate_recipe(form_data):
        is_valid = True
        #set flag to true, and if any user errors are found, set flag to false 
        if len(form_data['name']) < 2:
            flash("Please create a proper name for the recipe")
            is_valid = False

        if len(form_data['description']) < 3:
            flash("Please enter a proper description")
            is_valid = False    

        if len(form_data['instructions']) < 3:
            flash("Please enter proper instructions for the recipe")
            is_valid = False      

        if 'under_30_minutes' not in form_data:
            flash("Please enter if the recipe is under 30 mins")
            is_valid = False               

        return is_valid