from flask import Blueprint
from app.controllers.home_controller import get_banner, get_articles, get_store
from flask_jwt_extended import jwt_required

home_routes = Blueprint('home_routes', __name__)

@home_routes.route('/banners', methods=['GET'])
@jwt_required()
def banners_route():
    return get_banner()

@home_routes.route('/articles', methods=['GET'])
@jwt_required()
def articles_route():
    return get_articles()

@home_routes.route('/store', methods=['GET'])
@jwt_required()
def store_route():
    return get_store()
