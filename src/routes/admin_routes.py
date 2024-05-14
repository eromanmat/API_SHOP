


from src import app
from src.controllers.accounts_controller import *
from src.controllers.admin_controller import *
from src.controllers.products_controller import *
from src.controllers.orders_controller import *
from src.middlewares import admin_account




@app.route('/admin/products', methods=['POST'])
@admin_account
def route_add_product():
    return add_product()

@app.route('/admin/products/<int:id>', methods=['DELETE'])
@admin_account
def route_delete_product(id):
    return delete_product(id)

@app.route('/admin/products/<int:id>', methods=['PUT'])
@admin_account
def route_edit_product(id):
    return edit_product(id)

@app.route('/admin/products/<int:id>', methods=['GET'])
@admin_account
def route_get_product_one(id):
    return get_product_one(id)

@app.route('/admin/products', methods=['GET'])
@admin_account
def route_get_products():
    return get_products()

@app.route('/admin/accounts/ban/<int:id>', methods=['POST'])
def route_ban_account(id):
    return ban_account(id)

@app.route('/admin/accounts/unban/<int:id>', methods=['POST'])
@admin_account
def route_unban_account(id):
    return unban_account(id)

@app.route('/admin/accounts/<int:id>', methods=['GET'])
@admin_account
def route_get_account_by_id(id):
    return get_account_by_id(id)

@app.route('/admin/orders', methods=['GET'])
@admin_account
def route_get_orders():
    return get_orders()

@app.route('/admin/orders/accept/<int:id>', methods=['POST'])
@admin_account
def route_change_order_state(id):
    return change_order_state(id)

@app.route('/admin/orders/cancel/<int:id>', methods=['POST'])
@admin_account
def route_cancel_order(id):
    return cancel_order(id)