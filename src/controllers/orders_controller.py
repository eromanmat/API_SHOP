


from src.utils import status_codes
from flask import jsonify, request
from src import db
from src.models import *
from flask_jwt_extended import get_jwt_identity




def create_order():
    try:
        data = request.get_json()

        product_id = data.get('product_id')


        if not product_id:
            return jsonify({'error': 'Not all data is available'}), status_codes['bad_request']

        email_token = get_jwt_identity()['email']
        product = Products.query.filter_by(id=product_id).first() 
        account = Accounts.query.filter_by(email = email_token).first() 

        if not product:
            return jsonify({'error': 'Product not found'}), status_codes['not_found']

        # Проверяем, забанен ли аккаунт перед созданием заказа
        if account.banned:
            return jsonify({'error': 'Account is banned'}), status_codes['no_access']

        # Проверяем наличие средств на балансе
        if account.balance < product.price:
            return jsonify({'error': "Not enough money on balance"}), status_codes['conflict']
        
        # Проверяем наличие достаточного количества товара перед созданием заказа
        if product.stock < 1: 
            return jsonify({'error': 'Not enough stock available'}), status_codes['conflict'] 
        
        account.balance -= product.price 

        # Уменьшаем количество товара в наличии
        product.stock -= 1

        # Создаем новый заказ
        new_order = Orders(product_id=product_id, account_id=account.id)
        db.session.add(new_order)
        db.session.commit()

        return jsonify({'message': 'Order created successfully'}), status_codes['created']

    except Exception as e:
        return jsonify({'error': str(e)}), status_codes['server_error']
    
def view_orders(): # -------------------------------------
    try:
        
        email_account = get_jwt_identity()['email']
        account = Accounts.query.filter_by(email=email_account).first()

        if not account:
            return jsonify({'error': "Account not found"}), status_codes['not_found']
        
        orders = Orders.query.filter_by(account_id=account.id).all()

        if not orders:
            return jsonify({"error": "Orders not found"}), status_codes['not_found']
        
        limit = request.args.get('limit', type = int)
        page = request.args.get('page', type = int)

        query = None

        if query:
            orders = query.paginate(page=page,per_page=limit,max_per_page=5, error_out=False) 
        else:
            orders = Orders.query.paginate(page=page,per_page=limit,max_per_page=5, error_out=False) 

        orders_info = []

        for order in orders.items:
            product = order.product
            type_product = product.type
            brand_product = product.brand

            order_data = {
                'id': order.id,
                'product_id': order.product_id,
                'product_name': product.name,  
                'product_price': product.price,
                'product_type': type_product,
                'product_brand': brand_product  
            }

            orders_info.append(order_data)

        return jsonify({
            'orders': orders_info,
            'count_products': orders.total,
            'count_pages':  orders.pages,
            'has_next': orders.has_next,
            'has_prev': orders.has_prev,
            'next_page': orders.next_num if orders.next_num else None,
            'prev_page': orders.prev_num if orders.prev_num else None
        })
       
    except Exception as e:
        return jsonify({'error': str(e)}), status_codes['server_error']