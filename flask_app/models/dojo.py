from flask_app.config.mysqlconnection import connectToMySQL
from .ninja import Ninja


class Dojo:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.ninjas = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dojos;"

        results = connectToMySQL('dojoninjas').query_db(query)
        dojos = []

        for dojo in results:
            dojos.append(cls(dojo))
        return dojos

    @classmethod
    def save(cls, data):
        query = "INSERT INTO dojos (name) VALUES (%(name)s);"
        result = connectToMySQL('dojoninjas').query_db(query, data)
        return result

    @classmethod
    def get_one_ninja(cls, data):
        query = "SELECT * FROM dojos LEFT JOIN ninjas on dojos.id = ninjas.dojo_id WHERE dojos.id = %(id)s;"
        results = connectToMySQL('dojoninjas').query_db(query, data)
        print(results)
        dojo = cls(results[0])
        for r in results:
            n = {
                'id': r['ninjas.id'],
                'first_name': r['first_name'],
                'last_name': r['last_name'],
                'age': r['age'],
                'created_at': r['ninjas.created_at'],
                'updated_at': r['ninjas.updated_at']
            }
            dojo.ninjas.append(Ninja(n))
        return dojo
