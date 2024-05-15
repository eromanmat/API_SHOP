


from src.utils import status_codes
from src.models import*
from src import db
from flask import jsonify,request

"""
    Нам доступна в продуктах фильтрация по типу и по бренду 
    Если фильтрация не отправлялась - отправить все продукты по лимиту и пейджу
    Если отправился тип - отбираем продукты по типу и отправляем их +-
    Если отправился бренд - отбираем продукту по бренду и отпрвляем их +-
    Если отправился и бренд и тип - отбираем и по тому и по тому и отправляем +-
"""

def view_products():
    try:
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


        #query = Products.query.filter(brand_id=3)
        # and_, or_, not_ 
        # query = Products.query.filter(Products.brand_id.in_([1, 3]))
        # query = Products.query.filter(Products.brand_id==3,Products.type_id == 2)
        # products = query.paginate(page=page,per_page=limit,max_per_page=5, error_out=False) 

        list_products = []

        for product in products.items:
            get_products = {'id':product.id, 'name':product.name, 'price':product.price}
            list_products.append(get_products)


        return jsonify({
            'products': list_products,
            'count_products': products.total,
            'count_pages':  products.pages,
            'has_next': products.has_next,
            'has_prev': products.has_prev,
            'next_page': products.next_num if products.next_num else None,
            'prev_page': products.prev_num if products.prev_num else None
        })
         
    except Exception as e:
        return jsonify({'error': str(e)}), status_codes['server_error']
    
def view_one_product(id):
    try:
        product = Products.query.get(id)

        if product:

            product_type = product.type.name
            product_brand = product.brand.name

            view_product = {'id': product.id, 'name': product.name, 'price': product.price, 'stock': product.stock, 'type': product_type, 'brand': product_brand}
            return jsonify(view_product)
        else:
            return jsonify({'error': 'Product not found'}), status_codes['not_found']

    except Exception as e:
        return jsonify({'error': str(e)}), status_codes['server_error']
    
