import json

import requests
from flask import Blueprint, request, render_template, current_app

from src.extensions import db
from src.models import Visitor

portfolio_bp = Blueprint('portfolio', __name__)


@portfolio_bp.route('/')
def index():
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    client_ip = x_forwarded_for[0] if x_forwarded_for else request.remote_addr
    current_app.logger.debug(f'Visitor ip: {client_ip}')

    try:
        visitor_infos = requests.get(f"https://ipapi.co/{client_ip}/json/").json()
        current_app.logger.debug(f'New visitor -: {visitor_infos}')
        current_app.logger.debug(f'Visitor - Details -: {visitor_infos}')

        visitor = Visitor(ip=client_ip, user_agent=request.headers.get('User-Agent'),
                          description=json.dumps(visitor_infos))

        db.session.add(visitor)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        print(f'Error: {e}')

    return render_template("portfolio/index.html")
