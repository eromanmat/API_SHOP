

from flask import jsonify 
from src.utils import status_codes
from src.models import Accounts
from flask_jwt_extended import get_jwt_identity
from functools import wraps



#token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNTQzOTEzNCwianRpIjoiMzU0MGUzMTYtOWQxMC00ZjFjLTgzYmYtNjQwOWMzMDk2NDNhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJlbWFpbCI6ImFkbWluX3Rlc3RAZ21haWwuY29tIn0sIm5iZiI6MTcxNTQzOTEzNCwiY3NyZiI6IjgxYjdmODY1LTE4YTUtNDc1Ni05NjdjLTJkYjg3YTIzOGQyMiIsImV4cCI6MTcxNTQ4MjMzNH0.0-hXH6Jj3RFgj3n15y4mN-BQFNOCNN2CxJz1IXzztzA"



def admin_account(route):
    @wraps(route)
    def admin_login(*args, **kwargs):
        try:

            email_account = get_jwt_identity()['email']
            account = Accounts.query.filter_by(email=email_account).first()

            if account:
                if account.admin:
                    return route(*args, **kwargs)
                else:
                    return jsonify({"error": "No access"}), status_codes['no_access']
            else:
                return jsonify({'error': "Account not found"}), status_codes['not_found']

            
        except Exception as e:
            return jsonify({'error': str(e)}), status_codes['server_error']
        
    return admin_login