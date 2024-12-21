from flask import Blueprint
from app.controllers.tutorial_controller import get_tutorial
from flask_jwt_extended import jwt_required

tutorial_routes = Blueprint('tutorial_routes', __name__)

@tutorial_routes.route('/tutorials', methods=['GET'])
@jwt_required()
def tutorial_route():
    return get_tutorial()
