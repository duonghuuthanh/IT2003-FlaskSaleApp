from flask import render_template, request, redirect, session, jsonify
from app import app, dao, login
from flask_login import login_user, logout_user, login_required
import cloudinary.uploader
from app.decorators import annonymous_user
import utils
from app import admin


@app.route('/')
def index():
    cate_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    products = dao.load_products(category_id=cate_id, kw=kw)
    return render_template('index.html', products=products)


@app.route('/products/<int:product_id>')
def product_detail(product_id) :
    p = dao.get_product_by_id(product_id)
    return render_template('details.html', product=p)


@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ''
    if request.method == 'POST':
        password = request.form['password']
        confirm = request.form['confirm']
        if password.__eq__(confirm):
            # upload cloudinary
            avatar=''
            if request.files:
                res = cloudinary.uploader.upload(request.files['avatar'])
                avatar = res['secure_url']

            # Lưu user
            try:
                dao.register(name=request.form['name'],
                             username=request.form['username'],
                             password=request.form['password'],
                             avatar=avatar)
            except:
                err_msg = 'Đã có lỗi xảy ra! Vui lòng quay lại sau!'
            else:
                return redirect('/login')
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('register.html', err_msg=err_msg)


@app.route('/login', methods=['get', 'post'])
@annonymous_user
def login_my_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

            url_next = request.args.get('next')

            return redirect(url_next if url_next else '/')

    return render_template('login.html')


@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/login')


@app.route('/login-admin', methods=['post'])
def login_admin():
    username = request.form['username']
    password = request.form['password']

    u = dao.auth_user(username=username, password=password)
    if u:
        login_user(user=u)

    return redirect('/admin')


@app.route("/cart")
def cart():
    return render_template('cart.html')


@app.route('/cart', methods=['post'])
def add_to_cart():
    id = str(request.json['id'])

    key = app.config['MY_CART']
    cart = {} if key not in session else session[key]

    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else:
        name = request.json['name']
        price = request.json['price']
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        }

    session[key] = cart

    return jsonify(utils.cart_stats(cart=cart))


@app.route('/cart/<product_id>', methods=['put'])
def update_cart(product_id):
    key = app.config['MY_CART']
    cart = session.get(key)
    if cart and product_id in cart:
        quantity = request.json['quantity']
        cart[product_id]['quantity'] = int(quantity)

    session[key] = cart
    return jsonify(utils.cart_stats(cart=cart))


@app.route('/cart/<product_id>', methods=['delete'])
def delete_cart(product_id):
    key = app.config['MY_CART']
    cart = session.get(key)
    if cart and product_id in cart:
        del cart[product_id]

    session[key] = cart
    return jsonify(utils.cart_stats(cart=cart))


@app.route('/pay')
@login_required
def pay():
    key = app.config['MY_CART']
    cart = session.get(key)
    err_msg = ''
    if cart:
        if dao.add_receipt(cart=cart):
            del session[key]
        else:
            err_msg = 'Dữ liệu hóa đơn bị lỗi!'
    else:
        err_msg = 'Không có giỏ hàng!'

    return {'err_msg': err_msg}


@app.context_processor
def common_data():
    categories = dao.load_categories()

    return {
        'categories': categories,
        'cart': utils.cart_stats(session.get(app.config['MY_CART']))
    }


@login.user_loader
def user_load(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    app.run(debug=True)
