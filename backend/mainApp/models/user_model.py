from database.db import db 
class Users(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer,primary_key =True)
    username = db.Column(db.String(),nullable =False)
    email = db.Column(db.String(),nullable =False)
    password = db.Column(db.String(),nullable =False)
    provider = db.Column(db.String(),nullable =False)
    