#!/usr/bin/env python3
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty=db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

class ProductSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "price", "qty")

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@app.route("/", methods=["GET"])
def hello():
    return "Hello,  MOH!"

@app.route("/product", methods=["POST"])
def add_product():
    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]
    qty = request.json["qty"]

    new_product = Product(name, description, price, qty)
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)

@app.route("/product", methods=["GET"])
def get_products():
    all_product = Product.query.all()
    result = products_schema.dump(all_product)
    return jsonify(result)

@app.route("/product/<id>", methods=["GET"])
def one_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

@app.route("/product/<id>", methods=["PUT"])
def update_product(id):
    last_product = Product.query.get(id)
    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]
    qty = request.json["qty"]
    last_product.name = name
    last_product.description = description
    last_product.price = price
    last_product.qty = qty
    db.session.commit()
    return product_schema.jsonify(last_product)

@app.route("/product/<id>", methods=["DELETE"])
def delete_product(id):
    last_product = Product.query.get(id)
    db.session.delete(last_product)
    db.session.commit()
    return jsonify({
        "code": 202,
        "msg": "product delete",
    })

if __name__ == "__main__":
    app.run(debug=True)