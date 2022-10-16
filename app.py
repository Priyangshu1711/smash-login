from flask import Flask , render_template , request , redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField , BooleanField
from wtforms.validators import InputRequired , Email , Length   



app  = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'skey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16) , unique =True)
    email = db.Column(db.String(50) , unique =True)
    password = db.Column(db.String(80))

class LoginForm(FlaskForm):
    username = StringField('username',  validators=[InputRequired() , Length(min= 4 , max =16)])
    password = PasswordField('password',  validators=[InputRequired() , Length(min=8 , max =80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired() ,Email(message = 'invalid email'),Length(max=50)])
    username = StringField('username',  validators=[InputRequired() , Length(min= 4 , max =16)])
    password = PasswordField('password',  validators=[InputRequired() , Length(min=8 , max =80)])

@app.route('/' , methods = ['GET', 'POST'])
def index():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if(user.password == form.password.data):
                return render_template('welcome.html')
        return '<h1>Ivalid username or password </h1>'
   
    return render_template('index.html' , form = form) 

@app.route('/about')   
def about():
    return render_template('about.html')

@app.route('/contact') 
def contact():
    return render_template('contact.html')

@app.route('/service') 
def service():
    return render_template('service.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/signup' , methods = ['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        newuser = User(username = form.username.data , email = form.email.data , password = form.password.data)
        db.session.add(newuser)
        db.session.commit()

        return '<h1>New user has been created!</h1>'

        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'    
    return render_template('signup.html' , form = form) 
if __name__ == '__main__':
    app.run(debug=True)