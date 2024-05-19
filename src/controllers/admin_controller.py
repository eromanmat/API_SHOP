


from src.utils import status_codes
from flask import jsonify, request
from src import db
from src.models import *



def add_product():
    try:
        # Получение данных из JSON-запроса
        data = request.get_json()

        # Извлечение данных из JSON
        product_name = data.get('name')
        product_price = data.get('price')
        product_stock = data.get('stock')
        product_type_id = data.get('type_id')
        product_brand_id = data.get('brand_id')
        
        # Проверка наличия всех обязательных данных
        if not all([product_name, product_price, product_stock]):
            return jsonify({'error': 'not correct params in request'}), status_codes['bad_request']

        # ------------------------------- Добавить проверки по таблице -----------------------------------------
        if type(product_name) != str:
            return jsonify({'error': 'not correct params in request. Name must by type string'}), status_codes['bad_request']

        if len(product_name) > 20 or len(product_name) == 0:
            return jsonify({'error': 'not correct params in request. Name must by in range 1-20'}), status_codes['bad_request']
            

        # Создание нового продукта
        new_product = Products(name=product_name, price=product_price, stock=product_stock, type_id=product_type_id, brand_id=product_brand_id)

        # Добавление продукта в базу данных
        db.session.add(new_product)
        db.session.commit()

        return jsonify({'message': 'Product successfully added'}), status_codes['created']

    except Exception as e:
        return jsonify({'error': str(e)}), status_codes['server_error']
    

def delete_product(id):
    try:              
        product = Products.query.filter_by(id=id).first()
        if product:
            db.session.delete(product)
            db.session.commit()
            return jsonify({'message': 'Product deleted successfully'})
        else:
            return jsonify({'message': 'Product not found'}), status_codes['not_found']
    except Exception as e:
        return jsonify({'error': str(e)}), status_codes['server_error']
    

def edit_product(id):
    try:

        data = request.get_json()

        product_name = data.get('name')
        product_price = data.get('price')
        product_stock = data.get('stock')

        if product_name is None and product_price is None and product_stock is None:
            return jsonify({'message': 'Update fields were not sent'}), status_codes['bad_request']

        product = Products.query.filter_by(id=id).first()
        if product:
            if not product_name is None:
                product.name = product_name
            if not product_price is None:
                product.price = product_price
            if not product_stock is None:         
                product.stock = product_stock
            
            db.session.commit()
            return jsonify({'message':'Product successfully updated'})
        else:
            return jsonify({'message': 'product not found'}), status_codes['not_found']      
    except Exception as e:
        return jsonify({'error': str(e)}), status_codes['server_error']
    

def get_product_one(id):
    try:

        product = Products.query.filter_by(id=id).first()

        if product:
            # Продукт найден
            return jsonify({'id':product.id, 'name':product.name, 'price':product.price, 'stock':product.stock, 
                            'type_id':product.type_id, 'brand_id':product.brand_id})
        else:
            # Продукт не найден
            return jsonify({'message': "Product not found"}), status_codes['not_found']
    except Exception as e:
        return jsonify({'error': str(e)}), status_codes['server_error']
    

def get_products(): # -----------------------------------------
    try:

        data = request.args.to_dict()
        query = Products.query

        valid_data = {}
        
        for key,value in data.items():
            if key in Products.__table__.columns:
                valid_data[key] = value

        for key,value in valid_data.items():
            query = query.filter(getattr(Products, key) == value)

        products = query.all() # [Product,Product,Product]

        limit = request.args.get('limit', type = int)
        page = request.args.get('page', type = int)

        type_filter = request.args.get("type_id", type = int)
        brand_filter = request.args.get('brand_id', type = int)
        
        query = None

        if type_filter and brand_filter:
            query = Products.query.filter(Products.type_id==type_filter, Products.brand_id==brand_filter)
        elif type_filter:
            query = Products.query.filter(Products.type_id==type_filter)
        elif brand_filter: 
            query = Products.query.filter(Products.brand_id==brand_filter)

        
        if query:
            products = query.paginate(page=page,per_page=limit,max_per_page=5, error_out=False) 
        else:
            products = Products.query.paginate(page=page,per_page=limit,max_per_page=5, error_out=False)
        
        list_product = []
        for product in products.items:
            dict_product = {'name':product.name, 'price':product.price, 'stock':product.stock, 'type_id':product.type_id, 'brand_id':product.brand_id}
            list_product.append(dict_product)

        return jsonify({
            'products': list_product,
            'count_products': products.total,
            'count_pages':  products.pages,
            'has_next': products.has_next,
            'has_prev': products.has_prev,
            'next_page': products.next_num if products.next_num else None,
            'prev_page': products.prev_num if products.prev_num else None
        })
       
    except Exception as e:
        return jsonify({'error': str(e)}), status_codes['server_error']


def ban_account(id):
    # Может текущий аккаунт уже быть в бане - и нужно об этом уведомить 
    try:
        account = Accounts.query.filter_by(id=id).first()

        if account:  # Если учетная запись существует
            if not account.banned:  # Если учетная запись не заблокирована
                account.banned = True  # Устанавливаем флаг блокировки
                db.session.commit()  # Сохраняем изменения
                return jsonify({'message': 'Account successfully banned'})
            else:
                return jsonify({'message': 'Account already banned'}), status_codes['accepted']
        else:
            return jsonify({'message': 'Account not found'}), status_codes['not_found']
    except Exception as e:
        return jsonify({'error': str(e)}), status_codes['server_error']
    

def unban_account(id):
    # Может текущий аккаунт быть незаблокированным
    try:
        account = Accounts.query.filter_by(id=id).first()

        if account:  # Если учетная запись существует
            if account.banned:  # Если учетная запись заблокирована
                account.banned = False  # Убираем флаг блокировки
                db.session.commit()  # Сохраняем изменения
                return jsonify({'message': 'Account successfully unbanned'}), status_codes['ok']
            else:
                return jsonify({'message': 'Account already unbanned'}), status_codes['accepted']
        else:
            return jsonify({'message': 'Account not found'}), status_codes['not_found']
    except Exception as e:
        return jsonify({'error': str(e)}), status_codes['server_error']
    

def get_account_by_id(id):
    try:
        # Поиск аккаунта по идентификатору
        account = Accounts.query.filter_by(id=id).first()

        if account:
            # Возвращение информации о пользователе в виде JSON
            return jsonify({
                'id': account.id,
                'name': account.name,
                'email': account.email,
                'banned': account.banned
            })
        else:
            return jsonify({'message': 'Account not found'}), status_codes['not_found']
    except Exception as e:
        return jsonify({'error': str(e)}), status_codes['server_error']
    

def get_orders(): # ----------------------------------------------
    try:
        # Получение всех заказов
        orders = Orders.query.all()

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

        # Преобразование заказов в список словарей для возврата в JSON
        orders_date = [{'id': order.id, 'product_id': order.product_id, 'account_id': order.account_id, 'product_type': type_product, 'product_brand': brand_product}]

        orders_info.append(orders_info)

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
    

def change_order_state(id):
    try:
        # Поиск заказа по идентификатору
        order = Orders.query.filter_by(id=id).first()

        if order:
            # Установка статуса "утвержден" и сохранение изменений
            order.state_order = 1
            db.session.commit()
            return jsonify({'message': 'Order approved successfully'})
        else:
            return jsonify({'message': 'Order not found'}), status_codes['not_found']
    except Exception as e:
        return jsonify({'error': str(e)}), status_codes['server_error']
    

def cancel_order(id):
    try:
        # Поиск заказа по идентификатору
        order = Orders.query.filter_by(id=id).first()

        if order:
            # Установка статуса "отменен" и сохранение изменений
            order.state_order = 2
            db.session.commit()
            return jsonify({'message': 'Order cancelled successfully'})
        else:
            return jsonify({'message': 'Order not found'}), status_codes['not_found']
    except Exception as e:
        return jsonify({'error': str(e)}), status_codes['server_error']
    

