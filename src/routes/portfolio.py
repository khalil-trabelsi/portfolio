import json

import requests
from flask import Blueprint, request, render_template, current_app

from src.extensions import db
from src.models import Visitor

portfolio_bp = Blueprint('portfolio', __name__)


@portfolio_bp.route('/')
def index():
    remote_addr = request.remote_addr
    current_app.logger.info(f'{remote_addr}')
    visitor_infos = requests.get(f"https://ipapi.co/{remote_addr}/json/").json()
    current_app.logger.info(f'New visitor -: {visitor_infos}')
    print(f'New visitor -: {visitor_infos}')

    visitor = Visitor(ip=remote_addr, user_agent=request.headers.get('User-Agent'),
                      description=json.dumps(visitor_infos))

    db.session.add(visitor)
    db.session.commit()

    return render_template("portfolio/index.html")
