from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os.path import abspath
from os import getcwd, environ

db_name = 'beeplanner.db'
app = Flask(__name__)
# uri = 'sqlite:///{}/{}'.format(abspath(getcwd()), db_name)
uri = environ['DATABASE_URL']
# uri = f'sqlite:///{abspath(getcwd())}/{db_name}'
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "gydasjhfuisuqtyy234897dshfbhsdfg83wt7"
# connection = f'mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}'
# db = create_engine()
db = SQLAlchemy(app)

# db = create_engine(connection)
# Base = db.Model
# Column = db.Column
# Integer = db.Integer
# String = db.String
# DateTime = db.DateTime
# Float = db.Float
# ForeignKey = db.ForeignKey
