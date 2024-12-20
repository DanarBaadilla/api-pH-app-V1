from flask import Blueprint
from app.controllers.home_controller import get_banner
from flask_jwt_extended import jwt_required

home_routes = Blueprint('home_routes', __name__)

@home_routes.route('/banners', methods=['GET'])
@jwt_required()
def banners_route():
    return get_banner()