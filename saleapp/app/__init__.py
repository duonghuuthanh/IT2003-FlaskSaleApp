from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babelex import Babel
import cloudinary

app = Flask(__name__)
app.secret_key = '12#^&*+_%&*)(*(&(*^&^$%$#((*65t87676'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/it03saledbv1?charset=utf8mb4' % quote('Admin@123')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MY_CART'] = 'cart'

db = SQLAlchemy(app=app)
login = LoginManager(app=app)
babel = Babel(app=app)
cloudinary.config(cloud_name='dxxwcby8l', api_key='448651448423589', api_secret='ftGud0r1TTqp0CGp5tjwNmkAm-A')


@babel.localeselector
def load_locale():
    return 'vi'
