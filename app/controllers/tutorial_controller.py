from flask import jsonify
from app.config.config import db

def get_tutorial_extract():
    try:
        # Query ke Firestore untuk mendapatkan data tutorial ekstrak
        mix_ref = db.collection('tutorials').document('f!xTutorials').collection('extract')
        results = mix_ref.stream()

        # List untuk menyimpan data tutorial ekstrak
        extracts_data = []

        for result in results:
            extract_data = result.to_dict()
            extracts_data.append(extract_data)

        # Return response JSON  
        response = {"extract": extracts_data}
        return jsonify(response), 200

    except Exception as e:
        # Return error message jika terjadi kesalahan
        return jsonify({"error": str(e)}), 500
        
def get_tutorial_mix():
    try:
        # Query ke Firestore untuk mendapatkan data tutorial mixProcedure
        mix_ref = db.collection('tutorials').document('f!xTutorials').collection('mixProcedure')
        results = mix_ref.stream()

        # List untuk menyimpan data tutorial mixProcedure
        mixing_data = []

        for result in results:
            mix_data = result.to_dict()
            mixing_data.append(mix_data)

        # Return response JSON  
        response = {"mixProcedure": mixing_data}
        return jsonify(response), 200

    except Exception as e:
        # Return error message jika terjadi kesalahan
        return jsonify({"error": str(e)}), 500

def get_tutorial_video():
    try:
        # Query ke Firestore untuk mendapatkan data video tutorial
        video_ref = db.collection('tutorials').document('f!xTutorials').collection('video')
        results = video_ref.stream()

        # Ambil data video pertama
        video_data = None
        for result in results:
            video_data = result.to_dict()
            break  # Hentikan loop setelah mendapatkan data pertama

        # Validasi jika tidak ada data
        if not video_data or 'urlVideo' not in video_data:
            return jsonify({"error": "No video data found or 'urlVideo' missing."}), 404

        # Return hanya urlVideo
        response = {"urlVideo": video_data['urlVideo']}
        return jsonify(response), 200

    except Exception as e:
        # Return error message jika terjadi kesalahan
        return jsonify({"error": str(e)}), 500
