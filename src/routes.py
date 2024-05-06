


from src import app
from src.controllers.accounts_controller import *
from src.controllers.admin_controller import *
from src.controllers.products_controller import *
from src.middlewares.banned_middleware import ban_unban
from flask_jwt_extended import jwt_required

@app.route('/admin/products', methods=['POST'])
def route_add_product():
    return add_product()

@app.route('/admin/products/<int:id>', methods=['DELETE'])
def route_delete_product(id):
    return delete_product(id)

@app.route('/admin/products/<int:id>', methods=['PUT'])
def route_edit_product(id):
    return edit_product(id)

@app.route('/admin/products/<int:id>', methods=['GET'])
def route_get_product_one(id):
    return get_product_one(id)

@app.route('/admin/products', methods=['GET'])
def route_get_products():
    return get_products()

@app.route('/admin/accounts/ban/<int:id>', methods=['POST'])
def route_ban_account(id):
    return ban_account(id)

@app.route('/admin/accounts/unban/<int:id>', methods=['POST'])
def route_unban_account(id):
    return unban_account(id)

@app.route('/admin/accounts/<int:id>', methods=['GET'])
def route_get_account_by_id(id):
    return get_account_by_id(id)

@app.route('/admin/orders', methods=['GET'])
def route_get_orders():
    return get_orders()

@app.route('/admin/orders/accept/<int:id>', methods=['POST'])
def route_change_order_state(id):
    return change_order_state(id)

@app.route('/admin/orders/cancel/<int:id>', methods=['POST'])
def route_cancel_order(id):
    return cancel_order(id)

@app.route('/accounts/invoice', methods=['POST'])
@ban_unban
def route_invoice():
    return invoice()

@app.route('/accounts/register', methods=['POST'])
def route_add_account():
    return add_account()

@app.route('/accounts/login', methods=['POST'])
def route_login_account():
    return login_account()

@app.route('/products', methods=['GET'])
@ban_unban
def route_view_products():
    return view_products()

@app.route('/products/<int:id>', methods=['GET'])
@ban_unban
def route_view_one_product(id):
    return view_one_product(id)

@app.route('/accounts/orders', methods=['POST'])
@jwt_required()
@ban_unban
def route_create_order():
    return create_order()

@app.route('/accounts/view_orders/<int:id>', methods=['GET'])
@ban_unban
def route_view_orders(id):
    return view_orders(id)


