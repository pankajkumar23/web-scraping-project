from database.db import db 

class MobileData(db.Model):
    __tablename__="mobile_data"
    id = db.Column(db.Integer,primary_key =True)
    mobile_name = db.Column(db.String(),nullable =False)
    description= db.Column(db.String(),nullable =False)
    price = db.Column(db.Float,nullable =False)
    
