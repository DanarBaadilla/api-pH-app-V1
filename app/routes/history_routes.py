from flask import Blueprint
from app.controllers.history_controller import get_history, get_detail_history, update_history, delete_history
from flask_jwt_extended import jwt_required

history_routes = Blueprint('history_routes', __name__)

@history_routes.route('/history', methods=['GET'])
@jwt_required()
def history_route():
    return get_history()

@history_routes.route('/history/<historyId>', methods=['GET'])
@jwt_required()
def detail_history_route(historyId):
    return get_detail_history(historyId)

@history_routes.route('/history/<historyId>', methods=['PATCH'])
@jwt_required()
def update_history_route(historyId):
    return update_history(historyId)

@history_routes.route('/history/<historyId>', methods=['DELETE'])
@jwt_required()
def delete_history_route(historyId):
    return delete_history(historyId)