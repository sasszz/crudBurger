from flask_app import app, render_template, request, redirect

from flask_app.models.topping import Topping
from flask_app.models.burger import Burger


# ! CREATE 
@app.route('/create/topping', methods = ['post'])
def create_topping():
    print(request.form)
    topping = Topping.save(request.form)
    return redirect('/toppings')

# ! READ ALL
@app.route('/toppings')
def topping():
    toppings = Topping.get_all()
    return render_template('newtopping.html', toppings = Topping.get_all())

# ! READ ONE
@app.route('/toppings/<int:id>')
def show_topping(id):
    data = {'id': id}
    topping = Topping.get_topping_with_burgers(data)
    burger =  Burger.get_burger_with_toppings(data)
    on_this_burger = []
    for burger in topping.on_burgers:
        on_this_burger.append(burger.name)
    print(on_this_burger)
    return render_template('show_topping.html', topping = topping, burger = burger, burgers = Burger.get_all(), on_this_burger = on_this_burger)

# ! ADD TOPPING 
@app.route('/add/topping', methods = ['post'])
def update_topping():
    print(request.form["burger_id"])
    Topping.update_topping(request.form)
    return redirect(f"/burgers/{request.form['burger_id']}")

# ! REMOVE TOPPING 
@app.route('/remove/topping', methods = ['post'])
def remove_topping():
    # print(request.form["burger_id"])
    Topping.remove_topping(request.form)
    return redirect(f"/burgers/{request.form['burger_id']}")