from mysqlconnection import connectToMySQL

class User: 
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at)" \
        "VALUES (%(first_name)s, %(last_name)s, %(email)s, NOW(), NOW());"

        user_id = connectToMySQL("user_schema").query_db(query, data)
        return user_id


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL("user_schema").query_db(query)
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
        results = connectToMySQL("user_schema").query_db(query, data)
        #results is a list of dictinosaries
        # results[0] is the dict at index 0
        #print(cls(results[0]))
        return (cls(results[0]))
        #return(cls(results[0]))
    
    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s ,  last_name = %(last_name)s ,  email= %(email)s ,  updated_at = NOW() WHERE id = %(id)s;"
        print(query)
        results = connectToMySQL("user_schema").query_db(query, data)

        return results

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        results = connectToMySQL("user_schema").query_db(query, data)
    

    
