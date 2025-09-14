import os

import click
from flask import Flask
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

from .extensions import db, migrate, mail
from .models import User
from .routes.admin import admin_bp
from .routes.auth import auth_bp
from .routes.portfolio import portfolio_bp


@click.command()
@with_appcontext
def init_db():
    db.create_all()

    admin_email = os.environ.get('ADMIN_EMAIL')
    admin_password = os.getenv('PASSWORD')

    if not admin_email or not admin_password:
        click.echo("ADMIN_EMAIL et PASSWORD are required")
        return

    user = User.query.filter_by(email=admin_email).first()
    if not user:
        hashed_password = generate_password_hash(password)
        user = User(username="Khalil TRABELSI", email=admin_email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        click.echo(f"User {user.username} created successfully")
    else:
        click.echo(f"User {user.username} already exists")


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'DEV'),
        ADMIN_EMAIL=os.getenv('ADMIN_EMAIL'),
        PASSWORD=os.getenv('PASSWORD'),
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "sqlite:///portfolio.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    app.register_blueprint(portfolio_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    app.cli.add_command(init_db)
    return app
