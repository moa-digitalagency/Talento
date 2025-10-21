from flask import Blueprint

bp = Blueprint('api_v1', __name__, url_prefix='/api/v1')

from app.routes.api_v1 import auth, users, talents, cinema, stats, exports
