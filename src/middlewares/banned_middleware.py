

from flask import jsonify
from src.models import Accounts
from src.utils import status_codes
from src import db, app
from functools import wraps
from flask_jwt_extended import JWTManager, get_jwt_identity




def ban_unban(route):
    @wraps(route)
    def account_status(*args, **kwargs):
        try:
            email_token = get_jwt_identity()['email']
            account = Accounts.query.filter_by(email=email_token).first()

            if account.banned:
                return jsonify({'mesage': ' Account is banned'}), status_codes['no_access']

            return route(*args, **kwargs)               
            
        except Exception as e:
            return jsonify({"status":"error",'message': str(e)}), status_codes['server_error']
    return account_status
