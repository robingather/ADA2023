from flask import Flask, request

from resources.product import Product, Products
from datetime import datetime, date, timedelta
from functools import wraps
from flask import Response

app = Flask(__name__)
product = Product()
products = Products()


def docache(minutes=5, content_type='application/json; charset=utf-8'):
    """ Flask decorator that allow to set Expire and Cache headers. """

    def fwrap(f):
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            r = f(*args, **kwargs)
            then = datetime.now() + timedelta(minutes=minutes)
            rsp = Response(r, content_type=content_type)
            rsp.headers.add('Expires', then.strftime("%a, %d %b %Y %H:%M:%S GMT"))
            rsp.headers.add('Cache-Control', 'public,max-age=%d' % int(60 * minutes))
            return rsp

        return wrapped_f

    return fwrap


@app.route('/products/', methods=['POST'])
def create_products():
    return products.post(request)


@app.route('/qproducts', methods=['POST'])
def create_products_from_query():
    return products.post_query(request)


@docache(minutes=4, content_type='application/json')
@app.route('/products/<string:pname>', methods=['GET'])
def get_order(pname):
    return product.get(pname)


@app.route('/products/<string:pname>/quantity', methods=['PUT'])
def update_order(pname):
    return product.put(pname, int(request.args.get('value')))


app.run(host='0.0.0.0', port=5000, debug=True)
