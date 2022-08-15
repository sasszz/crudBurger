from flask_app.config.mysqlconnection import connectToMySQL

# We need to import the topping class from our models
from flask_app.models import topping
from flask_app.models import restaurant
# burger.toppings.append( topping.Topping( topping_data ) )

DATABASE = 'burgers'

class Burger:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.bun = data['bun']
        self.meat = data['meat']
        self.calories = data['calories']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # We now create a list so that later we can add in all the topping objects that relate to a burger.
        self.toppings = []

    # This method will retrieve the burger with all the toppings that are associated with the burger.
    @classmethod
    def get_burger_with_toppings( cls , data ):
        query = "SELECT * FROM myburgers LEFT JOIN add_ons ON add_ons.burger_id = myburgers.id LEFT JOIN toppings ON add_ons.topping_id = toppings.id WHERE myburgers.id = %(id)s;"
        results = connectToMySQL('burgers').query_db( query , data )
        # results will be a list of topping objects with the burger attached to each row. 
        print(results)
        burger = cls( results[0] )
        for row_from_db in results:
            # Now we parse the topping data to make instances of toppings and add them into our list.
            topping_data = {
                "id" : row_from_db["toppings.id"],
                "topping_name" : row_from_db["topping_name"],
                "created_at" : row_from_db["toppings.created_at"],
                "updated_at" : row_from_db["toppings.updated_at"]
            }
            burger.toppings.append( topping.Topping( topping_data ) )
        return burger
    
    # ! READ ALL
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM myburgers;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DATABASE).query_db(query)
        # Create an empty list to append our instances of dojos
        burgers = []
        # Iterate over the db results and create instances of dojos with cls.
        for burger in results:
            burgers.append(cls(burger))
        return burgers

    # ! CREATE
    @classmethod
    def save(cls, data):
        print(data)
        query = "INSERT INTO myburgers (name, bun, meat, calories, restaurants_id) VALUES (%(name)s, %(bun)s, %(meat)s, %(calories)s, %(restaurants_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    # ! ADD TOPPING
    @classmethod
    def update_burger(cls, data):
        query = "INSERT INTO add_ons (topping_id, burger_id) VALUES (%(topping_id)s, %(burger_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    # ! EDIT BASICS
    @classmethod
    def edit_burger(cls, data):
        query = "UPDATE myburgers SET name = %(name)s, bun = %(bun)s, meat = %(meat)s WHERE id = %(burger_id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)