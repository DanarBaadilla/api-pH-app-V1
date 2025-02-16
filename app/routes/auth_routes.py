from flask import Blueprint
from app.controllers.auth_controller import register_guest, activate_server

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/server', methods=['GET'])
def server_route():
    return activate_server()

@auth_routes.route('/registerGuest', methods=['POST'])
def register_route():
    return register_guest()