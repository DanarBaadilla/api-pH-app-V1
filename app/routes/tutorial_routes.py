from flask import Blueprint
from app.controllers.tutorial_controller import get_tutorial_extract, get_tutorial_mix, get_tutorial_video
from flask_jwt_extended import jwt_required

tutorial_routes = Blueprint('tutorial_routes', __name__)

@tutorial_routes.route('/extract', methods=['GET'])
@jwt_required()
def extract_route():
    return get_tutorial_extract()

@tutorial_routes.route('/mix', methods=['GET'])
@jwt_required()
def mix_route():
    return get_tutorial_mix()

@tutorial_routes.route('/video', methods=['GET'])
@jwt_required()
def video_route():
    return get_tutorial_video()