import json

import requests
from flask import Blueprint, request, render_template, current_app

from src.extensions import db
from src.models import Visitor

portfolio_bp = Blueprint('portfolio', __name__)


@portfolio_bp.route('/')
def index():
    x_forwarded_for = request.headers.get('X-Forwarded-For', [])
    client_ip = x_forwarded_for[0] if x_forwarded_for else request.remote_addr
    current_app.logger.debug(f'Visitor ip: {client_ip}')

    try:
        print(x_forwarded_for[0])
        print(client_ip)
        visitor_infos = requests.get(f"https://ipapi.co/{client_ip}/json/").json() if client_ip else "No data"
        current_app.logger.debug(f'New visitor -: {visitor_infos}')
        current_app.logger.debug(f'Visitor - Details -: {visitor_infos}')
        visitor_detail = {
            "ip": client_ip,
            "city": visitor_infos.get("city"),
            "region": visitor_infos.get("region"),
            "country": visitor_infos.get("country_name"),
            "latitude": visitor_infos.get("latitude"),
            "longitude": visitor_infos.get("longitude")
        }
        visitor = Visitor(ip=client_ip, user_agent=request.headers.get('User-Agent'),
                          description=json.dumps(visitor_detail))

        db.session.add(visitor)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        print(f'Error: {e}')

    return render_template("portfolio/index.html")
