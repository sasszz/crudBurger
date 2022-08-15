from flask_app.config.mysqlconnection import connectToMySQL

# from flask_app.models import restaurant
from flask_app.models import burger

DATABASE = 'burgers'

class Restaurant:
    def __init__( self, data ):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.burgers = []
    
    # ! READ ALL
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM restaurants;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DATABASE).query_db(query)
        # Create an empty list to append our instances of restaurants
        restaurants = []
        # Iterate over the db results and create instances of restaurants with cls.
        for restaurant in results:
            restaurants.append( cls(restaurant) )
        return restaurants

    # ! READ/RETRIEVE ONE
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM restaurants WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        restaurant = Restaurant(result[0])
        return restaurant

    # ! READ/RETRIEVE ONE WITH BURGERS
    @classmethod
    def get_one_with_burgers(cls,data):
        query = "SELECT * FROM restaurants LEFT JOIN myburgers ON restaurants.id = myburgers.restaurants_id WHERE restaurants.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        restaurant = Restaurant(results[0])
        for result in results:
            temp_burger = {
            'id' : result['myburgers.id'],
            'name' : result['myburgers.name'],
            'bun' : result['bun'],
            'meat' : result['meat'],
            'calories' : result['calories'],
            'created_at' : result['myburgers.created_at'],
            'updated_at' : result['myburgers.updated_at'],
            'restaurants_id' : result['restaurants_id'],
            }
            restaurant.burgers.append(burger.Burger(temp_burger))
        return restaurant

    # ! CREATE
    @classmethod
    def save_restaurant(cls, data):
        query = "INSERT INTO restaurants (name) VALUES (%(name)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    # ! UPDATE
    @classmethod
    def update(cls,data):
        query = "UPDATE restaurants SET first_name = %(first_name)s, last_name = %(last_name)s, age = %(age)s, dojo_id = %(dojo_id)s WHERE id = %(id)s ;"
        return connectToMySQL(DATABASE).query_db(query, data)


    # ! DELETE
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM restaurants WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)