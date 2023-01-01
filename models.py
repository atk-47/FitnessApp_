from .main import db, UserMixin

#different databases as Classes
class Test(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))

class User_details(UserMixin,db.Model):
    Uid = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(30))
    dob = db.Column(db.Date)
    phone = db.Column(db.Integer)
    addressLine1 = db.Column(db.String(50))
    city = db.Column(db.String(30))
    pincode = db.Column(db.Integer)