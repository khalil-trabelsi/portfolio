from flask import Blueprint, render_template, request, url_for

from src import db
from src.models import Visitor
from src.routes.auth import login_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')


@admin_bp.route('/visitors')
def get_visitors():
    query = Visitor.query.order_by(Visitor.visited_at.desc())
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 9, type=int)

    visitors = db.paginate(query, page=page, per_page=per_page, error_out=False)
    next_url = url_for('admin.get_visitors', page=visitors.next_num) if visitors.has_next else None
    prev_url = url_for('admin.get_visitors', page=visitors.prev_num) if visitors.has_prev else None

    return render_template("admin/visitors_table.html", visitors=visitors.items, next_url=next_url, prev_url=prev_url,
                           current_page=page)
