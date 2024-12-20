from flask import Blueprint
from app.controllers.auth_controller import register_guest

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/register', methods=['POST'])
def register_route():
    return register_guest()