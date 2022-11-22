from app.models import Category, Product, User, Receipt, ReceiptDetails
from app import db
from flask_login import current_user
import hashlib


def load_categories():
    return Category.query.all()


def load_products(category_id=None, kw=None):
    query = Product.query

    if category_id:
        query = query.filter(Product.category_id == category_id)

    if kw:
        query = query.filter(Product.name.contains(kw))

    return query.all()


def get_product_by_id(product_id):
    return Product.query.get(product_id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def register(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, username=username, password=password, avatar=avatar)
    db.session.add(u)
    db.session.commit()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def add_receipt(cart):
    if cart:
        """
            {
                "1" : {
                    "id": "...",
                    "name": "...",
                    "price": "...",
                    "quantity": "..."
                },
                "2" : {
                    "id": "...",
                    "name": "...",
                    "price": "...",
                    "quantity": "..."
                }
            }
        """
        r = Receipt(user=current_user)
        db.session.add(r)
        for c in cart.values():
            d = ReceiptDetails(quantity=c['quantity'],
                               price=c['price'],
                               receipt=r,
                               product_id=int(c['id']))
            db.session.add(d)
        try:
            db.session.commit()
        except:
            return False
        else:
            return True
