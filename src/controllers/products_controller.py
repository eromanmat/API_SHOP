


from src.utils import status_codes
from src.models import*
from src import db
from flask import jsonify


def view_products():
    try:
        products = Products.query.all()
        list_products = []

        for product in products:
            get_products = {'id':product.id, 'name':product.name, 'price':product.price}
            list_products.append(get_products)
        return jsonify(list_products)
         
    except Exception as e:
        return jsonify({'error': str(e)}), status_codes['server_error']
    
def view_one_product(id):
    try:
        product = Products.query.get(id)

        # Нужно найти по type_id сам type и отдавать его название

        # Нужно найти по brand_id сам brand и отдавать его название
        if product:

            product_type = product.type.name
            product_brand = product.brand.name

            view_product = {'id': product.id, 'name': product.name, 'price': product.price, 'stock': product.stock, 'type': product_type, 'brand': product_brand}
            return jsonify(view_product)
        else:
            return jsonify({'error': 'Product not found'}), status_codes['not_found']

    except Exception as e:
        return jsonify({'error': str(e)}), status_codes['server_error']
    
