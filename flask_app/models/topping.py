from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models import burger

DATABASE = 'burgers'

class Topping:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.topping_name = db_data['topping_name']
        # we need have a list in ="keyword from-rainbow">case we want to show which burgers are related to the topping.
        self.on_burgers = []
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save( cls , data ):
        query = "INSERT INTO toppings ( topping_name, created_at , updated_at ) VALUES (%(topping_name)s,NOW(),NOW());"
        return connectToMySQL('burgers').query_db(query, data)
    # This method will retrieve the specific topping along with all the burgers associated with it.

    @classmethod
    def get_topping_with_burgers( cls , data ):
        query = "SELECT * FROM toppings LEFT JOIN add_ons ON add_ons.topping_id = toppings.id LEFT JOIN myburgers ON add_ons.burger_id = myburgers.id WHERE toppings.id = %(id)s;"
        results = connectToMySQL('burgers').query_db( query , data )
        # results will be a list of topping objects with the burger attached to each row. 
        topping = cls( results[0] )
        for row_from_db in results:
            # Now we parse the topping data to make instances of toppings ="keyword from-rainbow">and add them into our list.
            burger_data = {
                "id" : row_from_db["myburgers.id"],
                "name" : row_from_db["name"],
                "meat" : row_from_db["meat"],
                "bun" : row_from_db["bun"],
                "calories" : row_from_db["calories"],
                "created_at" : row_from_db["myburgers.created_at"],
                "updated_at" : row_from_db["myburgers.updated_at"]
            }
            topping.on_burgers.append( burger.Burger( burger_data ) )
        return topping

    # ! READ ALL
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM toppings;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DATABASE).query_db(query)
        # Create an empty list to append our instances of toppings
        toppings = []
        # Iterate over the db results and create instances of toppings with cls.
        for topping in results:
            toppings.append( cls(topping) )
        return toppings

    # ! READ ALL EXCEPT
    @classmethod
    def get_all_except(cls):
        query = "SELECT * FROM toppings WHERE ;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DATABASE).query_db(query)
        # Create an empty list to append our instances of toppings
        toppings = []
        # Iterate over the db results and create instances of toppings with cls.
        for topping in results:
            toppings.append( cls(topping) )
        return toppings

    # ! READ/RETRIEVE ONE
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM toppings WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        topping = Topping(result[0])
        return topping

    # ! ADD TOPPING TO BURGER
    @classmethod
    def update_topping(cls, data):
        query = "INSERT INTO add_ons (burger_id, topping_id) VALUES (%(burger_id)s, %(topping_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    # ! REMOVE TOPPING TO BURGER
    @classmethod
    def remove_topping(cls, data):
        query = "DELETE FROM add_ons WHERE burger_id = %(burger_id)s AND topping_id = %(topping_id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)