from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('profile/dashboard.html', user=current_user)

@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    return render_template('profile/edit.html', user=current_user)

@bp.route('/view/<unique_code>')
def view(unique_code):
    from app.models.user import User
    user = User.query.filter_by(unique_code=unique_code.replace('-', '')).first_or_404()
    return render_template('profile/view.html', user=user)
