from socket import fromfd
from flask import Flask,render_template,request,session,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
from flask import url_for,flash
from flask_mail import Mail
import json


with open('config.json','r') as c:
    params = json.load(c)["params"]




#my db connection
local_server = True
app = Flask(__name__)
app.secret_key = 'prajwal'


#SMTP mail server settings
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='587',
    MAIL_USER_TLS=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-password']
)
mail=Mail(app)


#this is for getting user access
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:password@localhost/databas_table_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/ams'
db = SQLAlchemy(app)

# here we will create db models that is tables


class User (UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))

class Children(db.Model):
    cid=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    dob=db.Column(db.String(50),nullable=False)
    age=db.Column(db.Integer)
    sex=db.Column(db.String(50))
    nos=db.Column(db.Integer,primary_key=False)
    dis=db.Column(db.String(50),nullable=False)
    


class Staff(db.Model):
    sid=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(50))
    name=db.Column(db.String(50))
    dept=db.Column(db.String(50))
    number=db.Column(db.Integer)
    
class Trigr(db.Model):
    tid=db.Column(db.Integer,primary_key=True)
    cid=db.Column(db.Integer)

    name=db.Column(db.String(50))
    sex=db.Column(db.String(50))
    action=db.Column(db.String(50))
    time=db.Column(db.String(50))
    
class Application(db.Model):
    aid=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    dob=db.Column(db.String(50),nullable=False)
    addr=db.Column(db.String(500))
    phno=db.Column(db.Integer)
    idno=db.Column(db.Integer)
    ins=db.Column(db.String(500))
    status=db.Column(db.String(500))
    job=db.Column(db.String(500))
    det=db.Column(db.String(500),nullable=False)
    rs=db.Column(db.String(500),nullable=False)




#here we specify the end points and run the functions
@app.route("/")
def index():
    #a=Test.query.all()
    #print(a)
    #return render_template('index.html')
    return render_template('index.html')

@app.route('/application',methods=['POST','GET'])
def application():
    doct=db.engine.execute("SELECT * FROM `application`")

    if request.method == "POST":
        name=request.form.get('name')
        dob=request.form.get('dob')
        addr=request.form.get('addr')
        phno=request.form.get('phno')
        idno=request.form.get('idno')
        ins=request.form.get('ins')
        status=request.form.get('status')
        job=request.form.get('job')
        det=request.form.get('det')
        rs=request.form.get('rs')
        
        query=db.engine.execute(f"INSERT INTO `application` (`name`,`dob`,`addr`,`phno`,`idno`,`ins`,`status`,`job`,`det`,`rs`) VALUES ('{name}','{dob}','{addr}','{phno}','{idno}','{ins}','{status}','{job}','{det}','{rs}')")
        
        #mail.send_message('Adoption Managment System',sender=params['gmail-user'],recipients=[''],body='this is the first mail')
        #import pywhatkit as kit
        #from datetime import datetime
        
        flash("Application submitted successfull","info")
        #now=datetime.now()
        #current_time=now.strftime("%H")
        #time=now.strftime("%M")
        #p=int(current_time)
        #q=int(time)
        #kit.sendwhatmsg("+91phno","hello",p,q+1)
    return render_template('application.html',doct=doct)


@app.route('/staff',methods=['POST','GET'])
@login_required
def staff():
    if request.method == "POST":
        email=request.form.get('email')
        name=request.form.get('name')
        
        dept=request.form.get('dept')
        number=request.form.get('number')
        query=db.engine.execute(f"INSERT INTO `staff` (`email`,`name`,`dept`,`number`) VALUES ('{email}','{name}','{dept}','{number}')")
        flash("Information is saved",'primary')
    return render_template('staff.html')

@app.route('/sdisplay')
@login_required
def sdisplay():
    
    query=db.engine.execute("SELECT * FROM `staff`")
    return render_template('sdisplay.html',query=query)



@app.route('/children',methods=['POST','GET'])
@login_required
def children():
    doct=db.engine.execute("SELECT * FROM `children`")

    if request.method == "POST":
        name=request.form.get('name')
        dob=request.form.get('dob')
        age=request.form.get('age')
        sex=request.form.get('sex')
        nos=request.form.get('nos')
        dis=request.form.get('dis')
        
        query=db.engine.execute(f"INSERT INTO `children` (`name`,`dob`,`age`,`sex`,`nos`,`dis`) VALUES ('{name}','{dob}','{age}','{sex}','{nos}','{dis}')")
        
        #mail.send_message('Adoption Managment System',sender=params['gmail-user'],recipients=[''],body='this is the first mail')
        
        
        flash("New child has been added","info")
        
    #return render_template('patients.html',doct=doct)
    return render_template('children.html',doct=doct)

@app.route('/children_details')
@login_required
def children_details():
    
    query=db.engine.execute("SELECT * FROM `children`")
    return render_template('children_details.html',query=query)


@app.route("/edit/<string:cid>",methods=['POST','GET'])
@login_required
def edit(cid):
    posts=Children.query.filter_by(cid=cid).first()
    if request.method == "POST":
        
        name=request.form.get('name')
        dob=request.form.get('dob')
        age=request.form.get('age')
        sex=request.form.get('sex')
        nos=request.form.get('nos')
        dis=request.form.get('dis')
        
        db.engine.execute(f"UPDATE `children` SET `name` ='{name}',`dob` = '{dob}', `age` ='{age}',`sex`='{sex}',`nos`='{nos}',`dis`='{dis}' WHERE `children`.`cid`={cid}")
        flash("child details is updated","success")
        return redirect('/children_details')
    
    return render_template('edit.html',posts=posts)

@app.route("/delete/<string:cid>",methods=['POST','GET'])
@login_required
def delete(cid):
    db.engine.execute(f"DELETE FROM `children` WHERE `children`.`cid`={cid}")
    flash("Child Deleted Successfull","danger")
    return redirect('/children_details')


@app.route('/adoption_details')
@login_required
def adoption_details():
    query=db.engine.execute("SELECT * FROM `adopted`")
    return render_template('adoption_details.html',query=query)






@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists","warnings")
            return render_template('/signup.html')
        encpassword=generate_password_hash(password)
        new_user = db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")
        
        #this is method 2 to save data in database
        #newuser=User(username=username,email=email,password=encpassword)
        #db.session.add(newuser)
        #db.session.commit()
        flash("Signup Success Please Login", "success")
        return render_template('login.html')

    return render_template('signup.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success", 'primary')
            return redirect(url_for('index'))
        else:
            flash("invalid credentials","danger")
            return render_template('login.html')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout Successful","warning")
    return redirect(url_for('login'))





    
@app.route('/details')
@login_required
def details():
    posts=Trigr.query.all()
    return render_template('trigers.html',posts=posts)    

@app.route('/search',methods=['POST','GET'])
@login_required
def search():
    query=request.form.get('search')
    dept=Staff.query.filter_by(dept=query).first()
    name=Staff.query.filter_by(name=query).first()
    if name:
        flash("Staff is available","info")
    else:
        flash("Staff is not available","danger")    
    return render_template('index.html')    


@app.route('/home')
def home():
    return 'this is home'
app.run(debug=True)    

#username=current_user.username
