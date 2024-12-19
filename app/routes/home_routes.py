from flask import Blueprint
from app.controllers.home_controller import get_banner

home_routes = Blueprint('home_routes', __name__)

@home_routes.route('/banners', methods=['GET'])
def banners_route():
    return get_banner()