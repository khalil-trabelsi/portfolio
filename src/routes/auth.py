import functools
import secrets
import uuid

from flask import Blueprint, render_template, request, session, redirect, url_for, flash, g, abort
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms.fields.simple import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email

from src.models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == 'POST':
        if login_form.validate_on_submit():
            email = login_form.email.data
            password = login_form.password.data
            user = User.query.filter_by(email=email).first()
            error = None

            if user is None or not check_password_hash(user.password, password):
                error = 'Invalid email or password'

            if error is None:
                session.clear()
                session['user_id'] = user.id
                return redirect(url_for('admin.dashboard'))
            flash(error)
    return render_template("admin/login.html", login_form=login_form)


@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view