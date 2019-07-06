from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, fresh_login_required

#LoginManager-> is for instantiating the flask_login extension
#UserMixin -> includes a few methods that are needed for managing user login. If you dont want to implement these urself, use this.



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/sagar/Documents/SQLite_Database/flask_login_example/login.db'
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['USE_SESSION_FOR_NEXT'] = True #If user access a page after loggin out, redirect to login page and then this helps to take the user to the desired page. THe one that user chose after being logged out.This user choice is present as part of the request in a paramter called 'Next'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' #If user accesses a login_required page after being logged out, take them to the default login page instead of showing 'unauthorized page error' and show the below msg
login_manager.login_message = 'You really need to login!!!'
login_manager.refresh_view = 'login'
login_manager.needs_refresh_message = 'You need to re-login to access'

class User( UserMixin, db.Model ):
	id = db.Column( db.Integer, primary_key = True )
	username = db.Column( db.String(30), unique = True )


#flask_login needs below to deal with the actual user in your model
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
'''
@app.route('/')
def index():
	user = User.query.filter_by(username='sagar').first()
	if user:
		login_user(user)
		return 'You are now logged in!'
	else:
		return 'User not found!'
'''

@app.route('/login')		
def login():
	session['next'] = request.args.get('next')
	return render_template('login.html')

@app.route('/loggedin', methods=['POST'])
def loggedin():
	username = request.form['username']
	user = User.query.filter_by(username=username).first()
	if not user:
		return '<h1>User not found!</h1>'

	login_user(user, remember = True)
	if session.get('next'):
		return redirect(session['next'])
	

	return '<h1>You are now logged in!</h1>'


@app.route('/logout')
@login_required # User has to be logged-in first to logout
def logout():
	logout_user()
	return 'You are now logged out!'

@app.route('/home')
@login_required
def home():
	return 'The current user is '+ current_user.username

@app.route('/fresh')
@fresh_login_required
def fresh():
	return '<h1>You have a fresh login</h1>'

if __name__ == '__main__':
	app.run(debug=True)