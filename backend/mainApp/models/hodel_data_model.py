from database.db import db 
from sqlalchemy.dialects.postgresql import JSONB
class HotelData(db.Model):
    __tablename__="hotel_data"
    id = db.Column(db.Integer,primary_key =True)
    city_name = db.Column(db.String(),nullable =False)
    hotel_name = db.Column(db.String(),nullable =False, unique=True)
    price = db.Column(db.String(),nullable =True)
    dates=db.Column(JSONB,nullable =True)
    hotel_description = db.Column(db.Text())
    img_link = db.Column(JSONB,nullable =True)
    availability=db.Column(JSONB,nullable =True)
    
   
   
    
