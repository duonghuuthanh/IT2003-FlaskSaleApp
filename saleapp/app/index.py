from flask import render_template, request, redirect
from app import app, dao, login
from flask_login import login_user
from app import admin


@app.route('/')
def index():
    cate_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    products = dao.load_products(category_id=cate_id, kw=kw)
    return render_template('index.html',
                           products=products)


@app.route('/products/<int:product_id>')
def product_detail(product_id) :
    p = dao.get_product_by_id(product_id)
    return render_template('details.html', product=p)


@app.route('/login-admin', methods=['post'])
def login_admin():
    username = request.form['username']
    password = request.form['password']

    u = dao.auth_user(username=username, password=password)
    if u:
        login_user(user=u, force=True)

    return redirect('/admin')


@app.context_processor
def common_data():
    categories = dao.load_categories()

    return {
        'categories': categories
    }


@login.user_loader
def user_load(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    app.run(debug=True)
