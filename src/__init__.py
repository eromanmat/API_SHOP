


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store_database.db'

db = SQLAlchemy(app)

from src.routes.accounts_routes import *
from src.routes.admin_routes import *
from src.routes.products_route import *