from flask import jsonify, request
from app.config.config import db
import math

def get_banner():
    # Query ke Firestore untuk mendapatkan data banner
    banners_ref = db.collection('banners')
    results = banners_ref.stream()

    # list untuk menyimpan data banner
    banners_data = []

    for result in results:
        banner_data = result.to_dict()
        banners_data.append(banner_data)

    # return response json  
    response = {"banners": banners_data}
    return jsonify(response), 200

def articles():
    # query Parameters untuk pagination 
    size = request.args.get('size', type=int)
    page = request.args.get('page', type=int)

    # query ke firestore untuk mendapatkan data article
    articles_ref = db.collection('articles')

    # Hitung total data
    total_data = len(list(articles_ref.stream()))

    # Hitung total halaman
    total_pages = math.ceil(total_data / size)

    # Query untuk halaman tertentu
    query = articles_ref.limit(size).offset((page - 1) * size)
    results = query.stream()

    # list untuk menyimpan data article 
    article_data = []
    for result in results:
        article_info = result.to_dict()
        article_data.append(article_info)

    #return response
    response = {
        "meta": {
            "total_data": total_data,
            "total_pages": total_pages,
            "current_page": page,
            "data_per_page": size
        },
        "articles": article_data
    }

    return jsonify(response), 200