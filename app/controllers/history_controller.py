from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from app.config.config import db
from app.config.config import storage_client, GCS_BUCKET_NAME

def get_history():
    try:
        # Ekstrak userId dari token JWT
        userId = get_jwt_identity()

        # Referensi ke subcollection 'history' dari user dengan userId tertentu
        user_ref = db.collection('user').document(userId)
        history_ref = user_ref.collection('history')

        # Ambil semua dokumen dari subcollection 'history'
        history_docs = history_ref.stream()

        # Simpan hasil dalam bentuk list
        history_list = []
        for doc in history_docs:
            history_data = doc.to_dict()
            
            # field yang diperlukan
            filtered_data = {
                'historyId': history_data.get('historyId'),
                'name': history_data.get('name'),
                'tanggal': history_data.get('tanggal'),
                'pH': history_data.get('pH'),
            }
            history_list.append(filtered_data)

        # Jika tidak ada history, kembalikan respons 404
        if not history_list:
            return jsonify({"message": "No history found."}), 404

        # Kembalikan respons dengan data history
        return jsonify({"history": history_list}), 200
    
    # kembalikan respon untuk kode 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_detail_history(historyId):
    try:
        # Ekstrak userId dari token JWT
        userId = get_jwt_identity()

        # Referensi dokumen history berdasarkan historyId
        history_ref = db.collection('user').document(userId).collection('history').document(historyId)
        history_doc = history_ref.get()

        # Respon kode 404 jika dokumen tidak tersedia
        if not history_doc.exists:
            return jsonify({"error": "History not found"}), 404

        # Respon detail dokumen
        return jsonify(history_doc.to_dict()), 200

    except Exception as e:
        return jsonify({"error": "Failed to fetch history detail", "details": str(e)}), 500


def update_history(historyId):
    try:
        # Ekstrak userId dari token JWT
        userId = get_jwt_identity()

        # Data baru dari request body
        data = request.get_json()
        
        # Dictionary kosong untuk data yang akan diupdate
        updated_data = {}

        # Cek apakah name ada di request body
        if "name" in data:
            updated_data["name"] = data["name"]

        # Cek apakah description ada di request body
        if "description" in data:
            updated_data["description"] = data["description"]

        # Referensi dokumen history berdasarkan historyId
        history_ref = db.collection('user').document(userId).collection('history').document(historyId)
        history_doc = history_ref.get()

        # Respon 404 jika dokumen tidak ditemukan
        if not history_doc.exists:
            return jsonify({"error": "History not found"}), 404

        # Update dokumen jika ada dengan data yang akan diupdate
        if updated_data:
            history_ref.update(updated_data)

        # response update berhasil
        return jsonify({"message": "Update Successful."}), 200

    except Exception as e:
        return jsonify({"error": "Failed to update history", "details": str(e)}), 500




def delete_history(historyId):
    try:
        # Ekstrak userId dari token JWT
        userId = get_jwt_identity()

        # Referensi dokumen history berdasarkan historyId
        history_ref = db.collection('user').document(userId).collection('history').document(historyId)
        history_doc = history_ref.get()

        # Respon 404 jika dokumen tidak ditemukan
        if not history_doc.exists:
            return jsonify({"error": "History not found"}), 404

        # Ambil URL gambar dari Firestore
        history_data = history_doc.to_dict()
        name = history_data.get("name", "Unknown")  # Ambil name, default 'Unknown' jika tidak ada
        image_url = history_data.get("urlGambar")

        # Hapus gambar dari Google Cloud Storage jika ada URL gambar
        if image_url:
            try:
                # Ekstrak nama file dari URL (setelah bucket name)
                filename = image_url.split(f"https://storage.googleapis.com/{GCS_BUCKET_NAME}/")[-1]

                # Inisialisasi bucket dan hapus file
                bucket = storage_client.bucket(GCS_BUCKET_NAME)
                blob = bucket.blob(filename)    
                blob.delete()

                print(f"Gambar {filename} telah dihapus dari GCS.")
            except Exception as e:
                print(f"Gagal menghapus gambar dari GCS: {str(e)}")

        # Hapus dokumen dari Firestore
        history_ref.delete()

        return jsonify({"message": f"History with name '{name}' has been deleted."}), 200

    except Exception as e:
        return jsonify({"error": "Failed to delete history", "details": str(e)}), 500
