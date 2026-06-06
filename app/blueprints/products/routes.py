from flask import request

from app.blueprints.products import products_bp
from app.extensions import db
from app.models import Product


@products_bp.get("")
def get_products():
    # .all() fetches every product row from the products table.
    products = Product.query.all()

    return {
        "products": [product.to_dict() for product in products]
    }


@products_bp.get("/<int:product_id>")
def get_product(product_id):
    # get_or_404 finds by primary key or automatically returns a 404 error.
    product = Product.query.get_or_404(product_id)

    return {
        "product": product.to_dict()
    }


@products_bp.post("")
def create_product():
    data = request.get_json() or {}

    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    stock = data.get("stock", 0)
    image_url = data.get("image_url")

    # Basic validation keeps bad data from entering the database.
    if not name or price is None:
        return {"error": "Name and price are required."}, 400

    if price < 0:
        return {"error": "Price cannot be negative."}, 400

    if stock < 0:
        return {"error": "Stock cannot be negative."}, 400

    product = Product(
        name=name.strip(),
        description=description,
        price=price,
        stock=stock,
        image_url=image_url,
    )

    db.session.add(product)
    db.session.commit()

    return {
        "message": "Product created successfully.",
        "product": product.to_dict(),
    }, 201

@products_bp.put("/<int:product_id>")
def update_product(product_id):
    # First, find the product we want to update.
    # If it does not exist, Flask automatically returns a 404 response.
    product = Product.query.get_or_404(product_id)

    data = request.get_json() or {}

    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    stock = data.get("stock")
    image_url = data.get("image_url")

    # Only update fields that were actually sent in the request.
    # This lets the frontend update one field without resending everything.
    if name is not None:
        if not name.strip():
            return {"error": "Name cannot be empty."}, 400

        product.name = name.strip()

    if description is not None:
        product.description = description

    if price is not None:
        if price < 0:
            return {"error": "Price cannot be negative."}, 400

        product.price = price

    if stock is not None:
        if stock < 0:
            return {"error": "Stock cannot be negative."}, 400

        product.stock = stock

    if image_url is not None:
        product.image_url = image_url

    db.session.commit()

    return {
        "message": "Product updated successfully.",
        "product": product.to_dict(),
    }


@products_bp.delete("/<int:product_id>")
def delete_product(product_id):
    # Find the product first so we can return 404 if the ID is wrong.
    product = Product.query.get_or_404(product_id)

    db.session.delete(product)
    db.session.commit()

    return {
        "message": "Product deleted successfully."
    }