from flask import Flask
from utils.db import db
import pymysql
from routes.usuarios import usuarios
pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/apis'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# blueprints
app.register_blueprint(usuarios)