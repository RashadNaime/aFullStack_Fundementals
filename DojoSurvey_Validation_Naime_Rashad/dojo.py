from mysqlconnection import connectToMySQL
from flask import flash 

class Dojo: 
    def __init__(self, data):
        self.name = data['name']
        self.location = data['location']
        self.language = data['language']
        self.comments = data['comments']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO dojos (name, location, language, comments) 
            VALUES (%(name)s, %(location)s, %(language)s, %(comments)s);
        """

        dojo_id = connectToMySQL("dojo_survey_schema").query_db(query, data)
        return dojo_id


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dojos"
        results = connectToMySQL("dojo_survey_schema").query_db(query)
        print(results) #result is always a list of  dictionary
        all_dojos = []
        for row in results:
            all_dojos.append(cls(row))
        return all_dojos       

#every function except for get_all() requires a dictionary
    @classmethod
    def get_one(cls, data):
        #We must pass a dictionary into the query_db(query, data)
        query = "SELECT * FROM dojos WHERE id = %(id)s;"
        results = connectToMySQL("dojo_survey_schema").query_db(query, data)
        #results is a list of dictinosaries
        # results[0] is the dict at index 0
        #print(cls(results[0]))
        return (cls(results[0]))
        #return(cls(results[0]))
    
    @classmethod
    def update(cls, data):
        pass

    @classmethod
    def delete(cls, data):
        pass
            
    @staticmethod
    def validate(form):
        is_valid = True; 

        if len(form['name']) < 3:
            flash("The name entered is too short, put a proper name!")
            is_valid = False
        elif form['name'].isnumeric():
            flash("The name entered should not contain numbers!")
            is_valid = False 
        
        if len(form['location']) < 2:
            flash("The location entered is too short, put a proper name!")
            is_valid = False
        elif (form['location'].isnumeric()):
            flash("The location entered should not contain numbers!")
            is_valid = False

        if len(form['language']) < 1:
            flash("The language entered is too short, put a proper name!")
            is_valid = False          

        return is_valid