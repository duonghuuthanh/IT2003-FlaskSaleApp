from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
from flask_babelex import Babel
import cloudinary


app = Flask(__name__)
app.secret_key = '$#&*&%$(*&^(*^*&%^%$#^%&^%*&56547648764%$#^%$&^'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/it03saledbv2?charset=utf8mb4' % quote('Admin@123')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['CART_KEY'] = 'cart'

db = SQLAlchemy(app=app)
login = LoginManager(app=app)
babel = Babel(app=app)

cloudinary.config(cloud_name='dxxwcby8l', api_key='448651448423589', api_secret='ftGud0r1TTqp0CGp5tjwNmkAm-A')


@babel.localeselector
def load_locale():
    return 'vi'
