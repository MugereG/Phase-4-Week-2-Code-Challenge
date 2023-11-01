from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'

db = SQLAlchemy(app)

class RestaurantPizza(db.Model):
  __tablename__ = 'restaurant_pizzas'

  id = db.Column(db.Integer, primary_key=True)
  price = db.Column(db.Float, nullable=False)
  pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
  restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)

  pizza = db.relationship('Pizza', back_populates='restaurant_pizzas')
  restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas')

  def __repr__(self):
    return '<RestaurantPizza {}>'.format(self.id)

class Pizza(db.Model):
  __tablename__ = 'pizzas'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  ingredients = db.Column(db.String(255), nullable=False)

  restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='pizza')

  def __repr__(self):
    return '<Pizza {}>'.format(self.id)

class Restaurant(db.Model):
  __tablename__ = 'restaurants'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  address = db.Column(db.String(255), nullable=False)

  restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='restaurant')

  def __repr__(self):
    return '<Restaurant {}>'.format(self.id)

if __name__ == '__main__':
  db.create_all()