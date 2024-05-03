


import requests # type: ignore
from src.utils import status_codes
from flask import jsonify, request
from src import db, app
from src.models import *
import re
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from datetime import timedelta
from API_SHOP import config
import secrets


jwt_secret_key = secrets.token_hex(12)
app.config['JWT_SECRET_KEY'] = jwt_secret_key
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

    

def invoice():
    data = request.get_json()

    sum = data.get('sum')
    account_id = data.get('account_id')
    crypto = data.get('crypto')


    resp = requests.post('https://testnet-pay.crypt.bot/api/createInvoice', json={"amount":sum, "asset":crypto}, headers={'Content-Type':'application/json', 'Crypto-Pay-API-Token':'11072:AANJ95ROJJ40qmu42JuEMQEbZgl4cWjWOZk'})

    print(resp.json())
    account_refill = Refill(money=sum, status_refill=0,check_id=resp.json()['result']['invoice_id'], account_id=account_id)
    db.session.add(account_refill)
    db.session.commit()
    return jsonify({"link":resp.json()['result']['pay_url']})

def add_account():
    try:
        data = request.get_json()

        new_name = data.get('name')
        new_email = data.get('email')
        new_password = data.get('password')


        email_check = r'^[a-zA-Z][a-zA-Z._%+-]{1,10}@[a-zA-Z]{1,15}\.[a-zA-Z]{2,4}$'
        password_check = r'^[^\s@]{4,10}$'

        hash_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        
        existing_account = Accounts.query.filter_by(email=new_email).first()

        if re.match(email_check, new_email) and re.match(password_check, new_password):
            if not all([new_name, new_email, new_password]):
                return jsonify({'error': 'not correct params in request'}), status_codes['bad_request']
            
        if existing_account:
            return jsonify({'error': 'Email already exists'}), status_codes['conflict']

        if type(new_name) != str:
            return jsonify({'error': 'not correct params in request. Name must by type string'}), status_codes['bad_request']

        if len(new_name) > 20 or len(new_name) == 0:
            return jsonify({'error': 'not correct params in request. Name must by in range 1-20'}), status_codes['bad_request']
        
        if len(new_email) > 30 or len(new_email) == 0:
            return jsonify({'error': 'not correct params in request. Email must by in range 1-20'}), status_codes['bad_request']
        
        if len(new_password) > 10 or len(new_password) == 0:
            return jsonify({'error': 'not correct params in request. Password must by in range 1-20'}), status_codes['bad_request']
            
        # Создание нового аккаунта
        new_account = Accounts(name=new_name, email=new_email, password=hash_password, banned=False)

        jwt_token = create_access_token(identity={'name': new_name}, expires_delta=timedelta(seconds=43200))

        # Добавление аккаунта в базу данных
        db.session.add(new_account)
        db.session.commit()

        #account_info = {'id': new_account.id, 'email': new_account.email}
        return jsonify({'token':jwt_token}), status_codes['created']


    except Exception as e:
        return jsonify({'error': str(e)}), status_codes['server_error']
    
def login_account():
    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        account_info = {'id': account.id, 'email': account.email}

        if email and password:
            account = Accounts.query.filter_by(email=email, password=password).first()
            if account:
                return jsonify({'message': 'Successful login', 'account_info': account_info}), status_codes['ok']
            else:
                return jsonify({'error': 'Invalid email or password'}), status_codes['bad_request']
        else:
            return jsonify({'message': 'Invalid email or password'}), status_codes['bad_request']
        
    except Exception as e:
        return jsonify({'error': str(e)}), status_codes['server_error']

def create_order():
    try:
        data = request.get_json()

        product_id = data.get('product_id')
        account_id = data.get('account_id')

        if not product_id or not account_id:
            return jsonify({'error': 'Not all data is available'}), status_codes['bad_request']

        product = Products.query.filter_by(id=product_id).first() 
        account = Accounts.query.filter_by(id=account_id).first() 

        if not product or not account:
            return jsonify({'error': 'Product or account not found'}), status_codes['not_found']

        # Проверяем, забанен ли аккаунт перед созданием заказа
        if account.banned:
            return jsonify({'error': 'Account is banned'}), status_codes['bad_request'] # Неверный статус

        # Проверяем наличие достаточного количества товара перед созданием заказа
        if product.stock < 1: 
            return jsonify({'error': 'Not enough stock available'}), status_codes['bad_request'] 

        # Уменьшаем количество товара в наличии
        product.stock -= 1

        # Создаем новый заказ
        new_order = Orders(product_id=product_id, account_id=account_id)
        db.session.add(new_order)
        db.session.commit()

        return jsonify({'message': 'Order created successfully'}), status_codes['created']

    except Exception as e:
        return jsonify({'error': str(e)}), status_codes['server_error']