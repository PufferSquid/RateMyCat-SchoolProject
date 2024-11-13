from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    
    def __init__(self, id : int, username : str, password : str):
        self.id = id
        self.username = username
        self.password = password
