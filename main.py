from flask import Flask, render_template,flash
from flask.globals import request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import login_required,logout_user,login_user,login_manager,LoginManager,current_user
from werkzeug.security import generate_password_hash,check_password_hash
#from .models import User_details, Test

#database connection
local_server = True
app = Flask(__name__)
app.secret_key = "ishan"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/workoutapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#different databases as Classes
class Test(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))

class User_details(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(30))
    dob = db.Column(db.Date)
    #phone = db.Column(db.Integer)
    password = db.Column(db.String(999))
    addressLine1 = db.Column(db.String(50))
    city = db.Column(db.String(30))
    pincode = db.Column(db.Integer)

# this is for getting the unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'


@login_manager.user_loader
def load_user(user_id):
    return User_details.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('index.html')
    #return render_template('pages-blank.html')

@app.route("/usersignup")
def usersignup():
    return render_template('usersignup.html')

@app.route('/signup',methods = ["POST","GET"])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        dob = request.form.get('dob')
        #password encryption
        encpassword = generate_password_hash(password,"sha256")

        emailUser = User_details.query.filter_by(email=email).first()
        if emailUser:
            flash("Email or srif is already taken","warning")
            return render_template("usersignup.html")
        new_user = db.engine.execute(f"INSERT INTO `user_details` (`name`,`email`,`password`,`dob`) VALUES ('{name}','{email}','{encpassword}','{dob}') ")
                
        flash("SignUp successful, kindly Login","success")
        return render_template("login.html")

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=="POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User_details.query.filter_by(email = email).first()
        #print(user)
        #print(user.password)
        #print(generate_password_hash(password,"sha256"))
        #print(check_password_hash(user.password,password))
        
        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","info")
            return render_template("index.html")#set to base for now
            #return 'logged in successfully'
        else:
            flash("Invalid Credentials","danger")
            return render_template("login.html")
            #return 'log in failed'

    return render_template("login.html")
        

@app.route('/test')
def test():
    try:
        a = Test.query.all()
        print(a)
        return 'mydb is connected'
    except Exception as e:
        print(e)
        return 'mydb not connected'


app.run(debug=True)


