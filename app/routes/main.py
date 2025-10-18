from flask import Blueprint, render_template, redirect, url_for

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return redirect(url_for('auth.register'))

@bp.route('/about')
def about():
    return render_template('about.html')
