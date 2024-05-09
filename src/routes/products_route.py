


from src import app
from src.controllers.products_controller import *
from src.middlewares.banned_middleware import ban_unban
from flask_jwt_extended import jwt_required



@app.route('/products', methods=['GET'])
def route_view_products():
    return view_products()

@app.route('/products/<int:id>', methods=['GET'])
def route_view_one_product(id):
    return view_one_product(id)