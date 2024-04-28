


from src import db

class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(10), nullable=False)
    banned = db.Column(db.Boolean, default=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

    type_id = db.Column(db.Integer, db.ForeignKey('types.id'), nullable=False)
    type = db.relationship('Types', backref=db.backref('products', lazy=True))

    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=False)
    brand = db.relationship('Brands', backref=db.backref('products', lazy=True))      

class Types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

class Brands(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('Products', backref=db.backref('orders', lazy=True))
    
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    account = db.relationship('Accounts', backref=db.backref('orders', lazy=True))
    # state_order = 0 1 2 | idle success cancel
    state_order = db.Column(db.Integer, default=0)
    

class Refill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    money = db.Column(db.Float, nullable=False, default=0)
    status_refill = db.Column(db.Integer, nullable=False)
    check_id = db.Column(db.Integer, nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    account = db.relationship('Accounts', backref=db.backref('refill', lazy=True))