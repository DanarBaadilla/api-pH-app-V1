import cv2
import os
import uuid
import numpy as np
from datetime import datetime
from app.config.config import db
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.models.LiquidSegmentation import segment_image
from app.models.pH_Classification import classify_ph
from app.config.config import GCS_BUCKET_NAME, GCS_BASE_URL, storage_client


def upload_image_to_gcs(image_data, filename, content_type):
    """Mengunggah file ke Google Cloud Storage dan mengembalikan URL publiknya."""
    try:
        # Inisialisasi klien GCS dengan kredensial
        bucket = storage_client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(filename)

        # Upload file ke bucket
        blob.upload_from_string(image_data, content_type=content_type)

        # Set file menjadi public agar bisa diakses
        blob.make_public()

        # Mengembalikan URL gambar yang diunggah
        return GCS_BASE_URL + filename
    
    except Exception as e:
        raise Exception(f"Gagal mengunggah gambar ke GCS: {str(e)}")

def predict():
    try:
        # Ekstrak userId dari token JWT
        userId = get_jwt_identity()

        # Validasi request body
        if 'name' not in request.form or 'image' not in request.files:
            return jsonify({"error": "Invalid input. 'name' and 'image' are required."}), 400

        name = request.form['name']
        image_file = request.files['image']

        # Ambil description jika ada, atau atur ke None
        description = request.form.get('description', None)

        # Validasi tipe file
        if not image_file.mimetype in ['image/jpeg', 'image/png']:
            return jsonify({"error": "Invalid file type. Only JPG, JPEG, and PNG are allowed."}), 400

        # Validasi ukuran file maksimal 5MB
        MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB dalam byte
        image_file.seek(0, os.SEEK_END)  # Pindah ke akhir file untuk cek ukuran
        file_size = image_file.tell()  # Dapatkan ukuran file
        image_file.seek(0)  # Kembalikan ke awal agar bisa dibaca lagi

        if file_size > MAX_FILE_SIZE:
            return jsonify({"error": "File size exceeds 5MB. Please upload a smaller image."}), 400

        # Baca data gambar
        image_data = image_file.read()

        # Load image ke dalam numpy array untuk diproses
        np_img = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        # Segmentasi gambar
        segmented_image = segment_image(image)
        if segmented_image is None:
            return jsonify({"error": "Segmentation failed or no liquid detected."}), 400

        # Generate nama file unik dalam folder user di GCS
        file_extension = image_file.filename.rsplit('.', 1)[-1].lower()
        filename = f"user/{userId}/{uuid.uuid4().hex}.{file_extension}"

        # Upload gambar ke GCS
        image_url = upload_image_to_gcs(image_data, filename, image_file.mimetype)

        # Klasifikasi nilai pH
        predicted_ph = classify_ph(segmented_image)

        # Ambil informasi tambahan dari koleksi "information" berdasarkan predicted_ph
        info_data = db.collection('information').document(str(predicted_ph)).get()

        if info_data.exists:
            info = info_data.to_dict().get('info', None)
            hex_color = info_data.to_dict().get('hex', None)
            judulPH = info_data.to_dict().get('judulPH', None)

        # Cari nilai historyId terbesar yang ada di Firestore
        user_ref = db.collection('user').document(userId)
        history_ref = user_ref.collection('history')

        existing_histories = history_ref.stream()
        max_id = 0  # Default jika belum ada history

        for doc in existing_histories:
            doc_id = doc.id  # Ambil historyId dari Firestore
            if doc_id.startswith("h"):
                try:
                    numeric_part = int(doc_id[1:])  # Ambil angka setelah "h"
                    max_id = max(max_id, numeric_part)  # Cari angka terbesar
                except ValueError:
                    continue  # Skip jika format salah

        # Generate history ID berikutnya
        history_id = f"h{max_id + 1:03d}"

        # Simpan data ke Firestore
        history_ref.document(history_id).set({
            "name": name,
            "description": description,  # Bisa None jika tidak diinputkan
            "historyId": history_id,
            "pH": predicted_ph,
            "tanggal": datetime.now().strftime("%d/%m/%Y"),
            "urlGambar": image_url  # URL gambar dari GCS
        })

        # Respons JSON
        response = {
            "name": name,
            "description": description,
            "historyId": history_id,
            "pH": predicted_ph,
            "judulPH": judulPH,
            "tanggal": datetime.now().strftime("%d/%m/%Y"),
            "urlGambar": image_url,
            "info": info,
            "hex": hex_color
        }
        return jsonify(response), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_example_photo():
    try:
        # Query ke Firestore untuk mendapatkan data contoh foto
        photo_ref = db.collection('tutorials').document('f!xTutorials').collection('exPhoto')
        results = photo_ref.stream()

        # List untuk menyimpan data foto
        photos_data = []

        for result in results:
            photo_data = result.to_dict()
            photos_data.append(photo_data)

        # Return response JSON  
        response = {"photos": photos_data}
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    