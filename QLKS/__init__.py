from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
from flask_babelex import Babel
import cloudinary


app = Flask(__name__)
app.secret_key = '&%^**Ygyugiuyg&^&*^*)^*&^R^&%&*UYFVYugIUGIU'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/qlksdb?charset=utf8mb4' % quote('Az2882000')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['CART_KEY'] = 'cart'
cloudinary.config(cloud_name='duxlhasjq', api_key='648295815347731', api_secret='A-U7OpxN-2jn2ZwahuxvKure10E')

db = SQLAlchemy(app=app)

login = LoginManager(app=app)
babel = Babel(app=app)


@babel.localeselector
def load_locale():
    return 'vi'