from flask import Flask, request, jsonify, make_response
from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza_restaurant.db'
db.init_app(app)


@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    restaurant_data = [{"id": r.id, "name": r.name, "address": r.address} for r in restaurants]
    return jsonify(restaurant_data)

@app.route('/restaurants/<int:restaurant_id>', methods=['GET'])
def get_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)

    if restaurant:
        pizzas = [{"id": p.id, "name": p.name, "ingredients": p.ingredients} for p in restaurant.pizzas]
        restaurant_data = {
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address,
            "pizzas": pizzas
        }
        return jsonify(restaurant_data)
    else:
        return make_response(jsonify({"error": "Restaurant not found"}), 404)

@app.route('/restaurants/<int:restaurant_id>', methods=['DELETE'])
def delete_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)

    if restaurant:
       
        RestaurantPizza.query.filter_by(restaurant_id=restaurant.id).delete()
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204
    else:
        return make_response(jsonify({"error": "Restaurant not found"}), 404)


@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    pizza_data = [{"id": p.id, "name": p.name, "ingredients": p.ingredients} for p in pizzas]
    return jsonify(pizza_data)


@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.json
    price = data.get("price")
    pizza_id = data.get("pizza_id")
    restaurant_id = data.get("restaurant_id")

    if price is None or pizza_id is None or restaurant_id is None:
        return make_response(jsonify({"errors": ["Missing required fields"]}), 400)

    if not (1 <= price <= 30):
        return make_response(jsonify({"errors": ["Price must be between 1 and 30"]}), 400)

    pizza = Pizza.query.get(pizza_id)
    restaurant = Restaurant.query.get(restaurant_id)

    if pizza and restaurant:
        restaurant_pizza = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
        db.session.add(restaurant_pizza)
        db.session.commit()

        return jsonify({"id": pizza.id, "name": pizza.name, "ingredients": pizza.ingredients})
    else:
        return make_response(jsonify({"errors": ["Invalid pizza or restaurant"]}), 400)

if __name__ == '__main__':
    app.run(debug=True)
