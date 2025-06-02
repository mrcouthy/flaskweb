from flask import Blueprint, render_template
from flask_login import current_user, login_required
from app.decorators import admin_required

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home')

@bp.route('/admin')
@login_required
@admin_required
def admin_page():
    return render_template('admin_page.html', title='Admin Page')
