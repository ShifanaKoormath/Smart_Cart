import json
from models.product import Product

def load_products(path="data/products.json"):
    with open(path, "r") as f:
        data = json.load(f)

    products = {}

    for p in data:
        product = Product(
            id=p["id"],
            name=p["name"],
            unit_weight=p.get("unit_weight"),
            price_per_unit=p.get("price_per_unit"),
            price_per_gram=p.get("price_per_gram")
        )
        products[product.id] = product

    return products
