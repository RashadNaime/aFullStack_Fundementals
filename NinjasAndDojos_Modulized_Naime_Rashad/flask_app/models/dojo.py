from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import ninja



class Dojo:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.ninjas = []


    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO dojos (name, created_at, updated_at)" \
        "VALUES (%(name)s, NOW(), NOW());"

        dojo_id = connectToMySQL("dojos_and_ninjas_schema").query_db(query, data)
        return dojo_id


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dojos"
        results = connectToMySQL("dojos_and_ninjas_schema").query_db(query)
        print(results) #result is always a list of  dictionary
        all_dojos = []
        for row in results:
            all_dojos.append(cls(row))
        return all_dojos   


    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM dojos JOIN ninjas ON dojos.id = ninjas.dojo_id WHERE dojos.id = %(id)s;"
        result = connectToMySQL("dojos_and_ninjas_schema").query_db(query, data)

        dojo = cls(result[0])
        for row in result:
            row_data = {
                "id": row['ninjas.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "age": row['age'],
                "created_at": row['ninjas.created_at'],
                "updated_at": row['ninjas.updated_at']                
            }
            dojo.ninjas.append(ninja.Ninja(row_data))
        print(row_data)

        return dojo

    @classmethod
    def update(cls, data):
        pass


    @classmethod
    def delete(cls, data):
        pass