from flask import render_template, request
from app import app
from app import dao


@app.route('/')
def index():
    categories = dao.load_categories()

    cate_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    products = dao.load_products(category_id=cate_id, kw=kw)
    return render_template('index.html',
                           categories=categories,
                           products=products)


@app.route('/products/<int:product_id>')
def product_detail(product_id):
    p = dao.get_product_by_id(product_id)
    return render_template('details.html', product=p)


if __name__ == '__main__':
    app.run(debug=True)
