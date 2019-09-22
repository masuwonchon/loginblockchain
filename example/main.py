"""
This is example web site using python flask based on LHB(login hash block) module.
@version: 1.0.0
@authour: suwonchon(suwonchon@gmail.com)
@contact http://github.com/masuwonchon/loginhashblock
@license: MIT
"""

from io import BytesIO
from flask import Flask, render_template, redirect, url_for, flash, session, abort, make_response, request
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required, Length, EqualTo
import onetimepass
import pyqrcode
import os
import base64
import sys

# import LHB library
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from loginhashblock.loginhashblock import *

DEBUG = True

# create application instance
app = Flask(__name__)
api = Api(app)
app.config.from_object('config')

# initialize extensions
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
lm = LoginManager(app)

class User(UserMixin, db.Model):
    """User model."""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    otp_secret = db.Column(db.String(16))
    Lhashblock = db.Column(db.String(128))
    LoginHB = str(Lhashblock)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.otp_secret is None:
            # generate a random secret
            self.otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def verify_LoginHB(self, LoginHB):
        loginhashblock = self.Lhashblock.split(',')
        return True

    def get_totp_uri(self):
        return 'otpauth://totp/2FA-Demo:{0}?secret={1}&issuer=2FA-Demo'.format(self.username, self.otp_secret)

    def verify_totp(self, token):
        return onetimepass.valid_totp(token, self.otp_secret)

    def get_username(self):
        return username

@lm.user_loader
def load_user(user_id):
    """User loader callback for Flask-Login."""
    return User.query.get(int(user_id))

class RegisterForm(FlaskForm):
    """Registration form."""
    username = StringField('Username', validators=[Required(), Length(1, 64)])
    password = PasswordField('Password', validators=[Required()])
    password_again = PasswordField('Password again', validators=[Required(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    """Login form."""
    username = StringField('Username', validators=[Required(), Length(1, 64)])
    password = PasswordField('Password', validators=[Required()])
    token = StringField('Token', validators=[Required(), Length(6, 6)])
    submit = SubmitField('Login')

# API Class
class index(Resource):
    def get(self):
        response = make_response(render_template('index.html'))
        return response

class register(Resource):
    def get(self):
        """User registration route."""
        if current_user.is_authenticated:
            # if user is logged in we get out of here
            return redirect(url_for('index'))

        form = RegisterForm()
        response = make_response(render_template('register.html', form=form))
        return response

    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        password_again = request.form.get('password_again')

        user = User.query.filter_by(username=username).first()

        if user is not None:
            flash('Username already exists.')
            return redirect(url_for('register'))

        # add new user to the database
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        # redirect to the two-factor auth page, passing username in session
        session['username'] = user.username

        return redirect(url_for('twofactor'))

class twofactor(Resource):
    def get(self):
        if 'username' not in session:
            return redirect(url_for('index'))

        user = User.query.filter_by(username=session['username']).first()

        if user is None:
            return redirect(url_for('index'))

        param = {'Cache-Control': 'no-cache, no-store, must-revalidate', 'Pragma': 'no-cache', 'Expires': '0'}
        response = make_response(render_template('two-factor-setup.html'), 200, param)
        return response

class qrcode(Resource):
    def get(self):
        #session['username'] = '11'

        if 'username' not in session:
            abort(404)

        user = User.query.filter_by(username=session['username']).first()

        if user is None:
            abort(404)

        # for added security, remove username from session
        del session['username']

        # render qrcode for FreeTOTP
        url = pyqrcode.create(user.get_totp_uri())
        stream = BytesIO()
        url.svg(stream, scale=3)
        param = {'Content-Type': 'image/svg+xml', 'Cache-Control': 'no-cache, no-store, must-revalidate','Pragma': 'no-cache', 'Expires': '0'}
        response = make_response(stream.getvalue(), 200, param)
        return response

class login(Resource):
    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        response = make_response(render_template('login.html'))

        return response

    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        token = request.form.get('token')
        prev_LHB = request.form.get('loginhashblock')

        user = User.query.filter_by(username=username).first()

        if not user:
            flash('not registered username')
            return make_response('Error', 302)

        if not username:
            flash('username is null')
            return make_response('Error', 302)

        if not password:
            flash('password is null')
            return make_response('Error', 302)

        #prev_LHB = 'AAA'

        if DEBUG:
            print_LHBlist(user.Lhashblock)

        if not prev_LHB:
            #if user is None or not user.verify_password(password) or not user.verify_totp(token):
            if user is None or not user.verify_password(password):
                print('[info:login:post] Invalid username, password or OTP token')
                flash('Invalid username, password or token.')
                return make_response('Error', 302)

            prev_LHB = get_loginhashblock()
            new_LHB = update_loginhashblock(prev_LHB)
            user.Lhashblock = new_LHB
            db.session.commit()

        else:
            if user is None or not user.verify_password(password):
                # Add LHB check logic
                print('[info:login:post:non_otp] Invalid username, password or token')
                flash('Invalid username, password or token.')
                return make_response('Error', 302)

            new_LHB = update_loginhashblock(prev_LHB)
            user.Lhashblock = new_LHB
            db.session.commit()

            if DEBUG:
                text = "[info:login:post]\nprev_hashblock[{}]: {}\nnext_hashblock[{}]: {}".format(username,prev_LHB,username,new_LHB)
                print(text)

        if not valid_loginhashblock(prev_LHB):
            flash('your account is hacked, You have to use OTP')
            return make_response('Error', 302)

        login_user(user)
        flash('You are now logged in!')
        condition = True
        response = make_response(render_template('index.html', condition=condition, username=username, LoginHB=new_LHB))
        return response

class logout(Resource):
    def post(self):
        username = request.form.get('username')
        prev_LHB = request.form.get('loginhashblock')

        if current_user.is_active == False:
            return redirect(url_for('index'))

        user = User.query.filter_by(username=username).first()

        if DEBUG:
            print_LHBlist(user.Lhashblock)

        if not prev_LHB:
            print("[info:logout:post] GO TO OTP")
        else:
            '''
            new_LHB = update_loginhashblock(prev_LHB)
            status, hblist = update_loginhashblocklist(user.Lhashblock, new_LHB)
            if status:
                user.Lhashblock = ",".join(hblist)
            else:
                hblist.append(new_LHB)
                user.Lhashblock = ",".join(hblist)

            db.session.commit()
            '''
            new_LHB = update_loginhashblock(prev_LHB)
            Lhashblock = update_loginhashblocklist(user.Lhashblock, new_LHB)
            user.Lhashblock = Lhashblock
            db.session.commit()

        condition = True
        logout_user()

        if DEBUG:
            text = "[info:logout:post]\nprev_hashblock[{}]: {}\nnext_hashblock[{}]: {}".format(username,prev_LHB,username,new_LHB)
            print(text)

        response = make_response(render_template('index.html', condition=condition, username=username, LoginHB=new_LHB))
        return response

    def get(self):
        if current_user.is_active == False:
            return redirect(url_for('index'))

        response = make_response(render_template('logout.html'))
        return response

class command(Resource):
    def get(self):
        response = make_response(render_template('clear.html'))
        return response

    def post(self):
        username = request.form.get('username')
        command = request.form.get('command')
        text = "[info:command] username: {}, command: {}".format(username, command)
        print(text)

        Set_hashblock = False

        if Set_hashblock:
            username="11"
            user = User.query.filter_by(username=username).first()
            user.Lhashblock=''
            db.session.commit()
            print('[info:login:get] login hash block is cleared in DB')

        command_num = 1
        return make_response(username, command_num)

# create database tables if they don't exist yet
db.create_all()

api.add_resource(index, '/')
api.add_resource(logout, '/logout')
api.add_resource(register, '/register')
api.add_resource(twofactor, '/twofactor')
api.add_resource(qrcode, '/qrcode')
api.add_resource(login, '/login')
api.add_resource(command, '/command')

@app.errorhandler(404)
def not_found(e):
    return '', 404

