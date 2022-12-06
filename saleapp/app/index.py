from flask import session
from app import app, dao, login, controllers
from app import utils
from app import admin


app.add_url_rule('/', 'index', controllers.index)
app.add_url_rule('/products/<int:product_id>', 'product-detail', controllers.product_detail)
app.add_url_rule('/register', 'register', controllers.register, methods=['get', 'post'])
app.add_url_rule('/login', 'login-user', controllers.login_my_user, methods=['get', 'post'])
app.add_url_rule('/logout', 'logout', controllers.logout_my_user)
app.add_url_rule('/login-admin', 'login-admin', controllers.login_admin, methods=['post'])
app.add_url_rule("/cart", 'cart', controllers.cart)
app.add_url_rule('/cart', 'add-cart', controllers.add_to_cart, methods=['post'])
app.add_url_rule('/cart/<product_id>', 'update-cart', controllers.update_cart, methods=['put'])
app.add_url_rule('/cart/<product_id>', 'delete-cart', controllers.delete_cart, methods=['delete'])
app.add_url_rule('/pay', 'pay', controllers.pay)
app.add_url_rule('/products/<product_id>/comments', 'comments', controllers.comments)
app.add_url_rule('/products/<product_id>/comments', 'comment-add', controllers.add_comment, methods=['post'])


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
