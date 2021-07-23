#Working on one to many 
#every single table should have a model file

from mysqlconnection import connectToMySQL
from flask_app.dog import Dog

class Collar: 
    def __init__(self, data):
        self.id = data['id']
        #self.dog_id = data['dog_id'] #replace this with a whole dog object
        self.dog = Dog.get_one({"id": data['dog_id']})
        self.color = data['color']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    
    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO collars (dog_id, color,created_at,updated_at)
            VALUES (%(dog_id)s, %(color)s, NOW(), NOW());
        """

        return connectToMySQL("dogs_schema").query_db(query,data)


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM collars"
        results = connectToMySQL("dogs_schema").query_db(query)
        print(results) #result is always a list of  dictionary
        collars = []
        for row in results:
            # row_data = {
            #     "id": row['id'],
            #     "dog": Dog.get_one({"id": row['dog_id']})
            #     "color" : row['color'],
            #     "created_at": row['created_at'],
            #     "updated_at": row['updated_at'],
            # }
            # all_users.append(cls(row_data))
            collars.append(cls(row))
        return all_users        



    @classmethod
    def get_one(cls, data):
        pass

    @classmethod
    def update(cls, data):
        pass

    @classmethod
    def delete(cls, data):
        pass