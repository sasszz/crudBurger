from flask_app import app, render_template, request, redirect
from flask_app.models.restaurant import Restaurant

# ! CREATE 
@app.route('/create/restaurant', methods = ['post'])
def create_restaurant():
    print(request.form)
    restaurant = Restaurant.save_restaurant(request.form)
    return redirect('/')

# ! READ ALL
@app.route('/restaurants')
def restaurant():
    restaurants = Restaurant.get_all()
    return render_template('restaurants.html', restaurants = Restaurant.get_all())

# ! READ ONE
@app.route('/restaurants/<int:id>')
def show_restaurant(id):
    data = {'id': id}
    restaurant = Restaurant.get_one_with_burgers(data)
    return render_template('show_restaurant.html', restaurant = restaurant)