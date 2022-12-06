from sqlalchemy import Column, Integer, Boolean, Float, String, Text, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from app import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime


class UserRoleEnum(UserEnum):
    USER = 1
    ADMIN = 2


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='category', lazy=False)

    def __str__(self):
        return self.name


prod_tag = db.Table('prod_tag',
                    Column('product_id', Integer, ForeignKey('product.id'), primary_key=True),
                    Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True))


class Product(BaseModel):
    __tablename__ = 'product'

    name = Column(String(50), nullable=False)
    description = Column(Text)
    price = Column(Float, default=0)
    image = Column(String(100))
    active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    tags = relationship('Tag', secondary='prod_tag',
                        lazy='subquery',
                        backref=backref('products', lazy=True))
    receipt_details = relationship('ReceiptDetails', backref='product', lazy=True)
    comments = relationship('Comment', backref='product', lazy=True)

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = Column(String(20), nullable=False, unique=True)

    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    email = Column(String(50))
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
    active = Column(Boolean, default=True)
    receipts = relationship('Receipt', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)


class Comment(BaseModel):
    content = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)

    def __str__(self):
        return self.content


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        c1 = Category(name='Điện thoại')
        c2 = Category(name='Máy tính bảng')
        c3 = Category(name='Phụ kiện')

        db.session.add(c1)
        db.session.add(c2)
        db.session.add(c3)

        db.session.commit()

        p1 = Product(name='iPhone 13 Pro Max', description='Apple, 256GB', price=35000000,
                     image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
                     category_id=1)
        p2 = Product(name='iPad Pro 2022', description='Apple, 128GB', price=32000000,
                     image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg',
                     category_id=2)
        p3 = Product(name='Sạc dự phòng', description='Apple, 16GB', price=24000000,
                     image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
                     category_id=3)
        p4 = Product(name='Galax Fold Z', description='Samsung, 256GB', price=33000000,
                     image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
                     category_id=1)
        p5 = Product(name='Galaxy Note Ultra 2022', description='Samsung, 128GB', price=32000000,
                     image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg',
                     category_id=1)
        p6 = Product(name='Apple Watch S7', description='Apple, 16GB', price=24000000,
                     image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
                     category_id=3)

        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)
        db.session.add(p4)
        db.session.add(p5)
        db.session.add(p6)

        db.session.commit()

        import hashlib

        password = str(hashlib.md5("123456".strip().encode('utf-8')).hexdigest())
        u1 = User(name='Thanh', username='admin', password=password,
                  avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
                  user_role=UserRoleEnum.ADMIN)

        u2 = User(name='Huu Thanh', username='dhthanh', password=password,
                  avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
                  user_role=UserRoleEnum.USER)

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
