from flask import Blueprint
from app.routes.anime import bp as bp_anime

bp = Blueprint("bp_api", __name__, url_prefix="/api")

bp.register_blueprint(bp_anime)
