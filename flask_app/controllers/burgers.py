from flask_app import app, render_template, request, redirect
from flask_app.models.burger import Burger
from flask_app.models.restaurant import Restaurant
from flask_app.models.topping import Topping

# ! CREATE 
@app.route('/create/burger', methods = ['post'])
def create_burger():
    print(request.form)
    burger = Burger.save(request.form)
    return redirect('/')

# ! READ ALL
@app.route('/')
def home():
    return render_template('home.html', burgers = Burger.get_all(), restaurants = Restaurant.get_all())

# ! READ ONE
@app.route('/burgers/<int:id>')
def show_burger(id):
    data = {'id': id}
    burger = Burger.get_burger_with_toppings(data)
    burger_toppings = []
    for topping in burger.toppings:
        burger_toppings.append(topping.topping_name)
    print(burger_toppings)
    return render_template('burgers.html', burger = burger, toppings = Topping.get_all(), burger_toppings = burger_toppings)

# # ! UPDATE
@app.route('/edit/burger', methods = ['post'])
def edit_burger():
    Burger.edit_burger(request.form)
    return redirect(f"/burgers/{request.form['burger_id']}")

# # ! DELETE 
# @app.route('/delete/<int:id>')
# def delete_burger(id):
#     Burger.destroy({'id': id})
#     return redirect('/')