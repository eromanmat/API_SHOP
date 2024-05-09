


from src import app
from src.controllers.accounts_controller import *
from src.controllers.products_controller import *
from src.controllers.orders_controller import *
from src.middlewares.banned_middleware import ban_unban
from flask_jwt_extended import jwt_required


@app.route('/accounts/invoice', methods=['POST'])
@jwt_required()
@ban_unban
def route_invoice():
    return invoice()

@app.route('/accounts/register', methods=['POST'])
def route_add_account():
    return add_account()

@app.route('/accounts/login', methods=['POST'])
def route_login_account():
    return login_account()

@app.route('/accounts/orders', methods=['POST'])
@jwt_required()
@ban_unban
def route_create_order():
    return create_order()

@app.route('/accounts/orders', methods=['GET'])
@jwt_required()
@ban_unban
def route_view_orders():
    return view_orders()