from flask import jsonify, request
from app.config.config import db
import math

def get_banner():
    try:
        # Query ke Firestore untuk mendapatkan data banner
        banners_ref = db.collection('banners')
        results = banners_ref.stream()

        # List untuk menyimpan data banner
        banners_data = []

        for result in results:
            banner_dict = result.to_dict()
            # Ambil hanya bannerId dan urlBanner
            banner_data = {
                "bannerId": banner_dict.get("bannerId"),
                "urlBanner": banner_dict.get("urlBanner")
            }
            banners_data.append(banner_data)

        # Return response JSON  
        response = {"banners": banners_data}
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_articles():
    try:
        # Query Parameters untuk pagination 
        size = request.args.get('size', type=int)
        page = request.args.get('page', type=int)

        # Validasi query parameters
        if size is None or page is None or size <= 0 or page <= 0:
            return jsonify({"error": "Invalid query parameters. 'size' and 'page' must be positive integers."}), 400

        # Query ke Firestore untuk mendapatkan data article
        articles_ref = db.collection('articles')

        # Hitung total data
        total_data = len(list(articles_ref.stream()))

        # Hitung total halaman
        total_pages = math.ceil(total_data / size)

        # Validasi halaman
        if page > total_pages:
            return jsonify({"error": f"Page {page} exceeds total pages {total_pages}."}), 400

        # Query untuk halaman tertentu
        query = articles_ref.limit(size).offset((page - 1) * size)
        results = query.stream()

        # List untuk menyimpan data article 
        article_data = []
        for result in results:
            article_info = result.to_dict()
            article_data.append(article_info)

        # Return response
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

    except Exception as e:
        # Return error message jika terjadi kesalahan
        return jsonify({"error": str(e)}), 500

def get_store():
    try:
        # Query ke Firestore untuk mendapatkan data store
        store_ref = db.collection('store')
        results = store_ref.stream()

        # List untuk menyimpan data store
        stores_data = []

        for result in results:
            store_data = result.to_dict()
            stores_data.append(store_data)

        # Return response JSON  
        response = {"stores": stores_data}
        return jsonify(response), 200

    except Exception as e:
        # Return error message jika terjadi kesalahan
        return jsonify({"error": str(e)}), 500
