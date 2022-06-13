import binascii
import os
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    token = db.Column(db.String(500), unique= True)
    name = db.Column(db.String(50), nullable= False)
    email = db.Column(db.String(100), nullable= False, unique= True)
    password = db.Column(db.String(500), nullable= False)

    def to_json(self):
        return {"id": self.id, "name": self.name, "email": self.email, "token": self.token}

    def generate_key(self):
        self.token = binascii.hexlify(os.urandom(20)).decode()
