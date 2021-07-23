#this is a model file 
#only returns objects, or list of objects, thats it
from mysqlconnection import connectToMySQL

class Dog:
    def __init__(self, data):
        #data we need to pass data from each field
        #match attributes to table fields
        self.id = data['id'] #data with field "id"
        self.name = data['name']
        self.age = data['age']
        self.hair_color = data['hair_color']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    
    #in general a CRUD applications needs 5 methods
    #create has 1 method 
    #READ has 2 methods
        # Read many things
        # Read 1 thing
    #update has 1 method
    #delete has 1 method
    #all of these methods are class methods

    @classmethod
    def create(cls, data):#data needs to be passed into database
        #pass #pass is a keyword that tells python to do nothin
        query = "INSERT INTO dogs (name, age, hair_color, created_at, updated_at) " \
            "VALUES (%(name)s, %(age)s, %(hair_color)s, NOW(), NOW());"
        #provide the schema to connnectToMySql
        dog_id = connectToMySQL("dogs_schema").query_db(query, data)
        return dog_id


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dogs"
        results = connectToMySQL("dogs_schema").query_db(query)
        print(results) #result is always a list of  dictionary
        all_dogs = []

        for row in results:
            all_dogs.append(cls(row))
        return all_dogs


    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM dogs WHERE id = %(id)s;"
        results = connectToMySQL("dogs_schema").query_db(query, data)

        #results is a list of dictinosaries
        # results[0] is the dict at index 0

        return(cls(results[0]))


    @classmethod
    def update(cls, data):
        pass


    @classmethod
    def delete(cls, data):
        pass