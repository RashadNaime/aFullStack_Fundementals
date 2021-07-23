from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
import re

class Email:
    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    
    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO emails (email)
            VALUES (%(email)s);
        """
        print(data)
        email_id = connectToMySQL("email_schema").query_db(query, data)
        return email_id


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM emails"
        results = connectToMySQL("email_schema").query_db(query)
        print(results) #result is always a list of  dictionary
        all_emails = []
        for row in results:
            all_emails.append(cls(row))
        return all_emails  


    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM emails WHERE email = %(email)s;"
        result = connectToMySQL("email_schema").query_db(query, data)

        # for row in result:
        #     row_data = {
        #         "id": row['ninjas.id'],
        #         "first_name": row['first_name'],
        #         "last_name": row['last_name'],
        #         "age": row['age'],
        #         "created_at": row['ninjas.created_at'],
        #         "updated_at": row['ninjas.updated_at']                
        #     }
        #     dojo.ninjas.append(ninja.Ninja(row_data))
        if len(result) == 1:
            return cls(result[0])
        else:
            return False

    @classmethod
    def update(cls, data):
        pass


    @classmethod
    def delete(cls, data):
        query = "DELETE FROM emails WHERE id = %(id)s;"
        results = connectToMySQL("email_schema").query_db(query, data)

    
    @staticmethod
    def validate(form):
        is_valid = True 
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

        if not EMAIL_REGEX.match(form['email']):
            flash("Invalid email format")
            is_valid = False 
        elif not Email.get_one({"email": form['email']}) == False:
            flash("The Email Already Exists")
            is_valid = False

        return is_valid


