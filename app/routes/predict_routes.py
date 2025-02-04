from flask import Blueprint
from app.controllers.predict_controller import predict, get_example_photo
from flask_jwt_extended import jwt_required

predict_routes = Blueprint('predict_routes', __name__)

@predict_routes.route('/predict', methods=['POST'])
@jwt_required()
def predict_image_route():
    return predict()

@predict_routes.route('/photo', methods=['GET'])
@jwt_required()
def photos_route():
    return get_example_photo()