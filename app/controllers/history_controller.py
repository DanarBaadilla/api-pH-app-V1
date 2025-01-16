from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.config.config import db

def get_history():
    try:
        # Ekstrak userId dari token JWT
        userId = get_jwt_identity()

        # Referensi ke subcollection 'history' dari user dengan userId tertentu
        user_ref = db.collection('user').document(userId)
        history_ref = user_ref.collection('history')

        # Ambil semua dokumen dari subcollection 'history'
        history_docs = history_ref.stream()

        # Simpan hasil dalam bentuk list dengan filter field yang diinginkan
        history_list = []
        for doc in history_docs:
            history_data = doc.to_dict()
            
            # Pilih hanya field yang diperlukan
            filtered_data = {
                'historyId': history_data.get('historyId'),
                'namaLarutan': history_data.get('namaLarutan'),
                'tanggal': history_data.get('tanggal'),
                'ph': history_data.get('ph'),
            }
            history_list.append(filtered_data)

        # Jika tidak ada history, kembalikan respons kosong
        if not history_list:
            return jsonify({"message": "No history found."}), 404

        # Kembalikan respons dengan data history
        return jsonify({"history": history_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_detail_history(historyId):
    try:
        # Ekstrak userId dari token JWT
        userId = get_jwt_identity()

        # Referensi dokumen history berdasarkan historyId
        history_ref = db.collection('user').document(userId).collection('history').document(historyId)
        history_doc = history_ref.get()

        # Cek apakah dokumen ada
        if not history_doc.exists:
            return jsonify({"error": "History not found"}), 404

        # Kembalikan detail dokumen
        return jsonify(history_doc.to_dict()), 200

    except Exception as e:
        return jsonify({"error": "Failed to fetch history detail", "details": str(e)}), 500


def update_history(historyId):
    try:
        # Ekstrak userId dari token JWT
        userId = get_jwt_identity()

        # Data baru dari request body
        data = request.get_json()
        updated_data = {
            "namaLarutan": data.get("namaLarutan"),
            "deskripsi": data.get("deskripsi")
        }

        # Referensi dokumen history berdasarkan historyId
        history_ref = db.collection('user').document(userId).collection('history').document(historyId)
        history_doc = history_ref.get()

        # Cek apakah dokumen ada
        if not history_doc.exists:
            return jsonify({"error": "History not found"}), 404

        # Update dokumen
        history_ref.update(updated_data)

        # Kembalikan data yang diperbarui
        updated_doc = history_ref.get()
        return jsonify(updated_doc.to_dict()), 200

    except Exception as e:
        return jsonify({"error": "Failed to update history", "details": str(e)}), 500


@jwt_required()
def delete_history(historyId):
    try:
        # Ekstrak userId dari token JWT
        userId = get_jwt_identity()

        # Referensi dokumen history berdasarkan historyId
        history_ref = db.collection('user').document(userId).collection('history').document(historyId)
        history_doc = history_ref.get()

        # Cek apakah dokumen ada
        if not history_doc.exists:
            return jsonify({"error": "History not found"}), 404

        # Hapus dokumen
        history_ref.delete()

        return jsonify({"message": f"History with ID {historyId} has been deleted."}), 200

    except Exception as e:
        return jsonify({"error": "Failed to delete history", "details": str(e)}), 500