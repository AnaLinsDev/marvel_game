from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/marvel_game'

db = SQLAlchemy(app)

from controller.UserController import *

if __name__=='__main__':
    app.run(debug=True)