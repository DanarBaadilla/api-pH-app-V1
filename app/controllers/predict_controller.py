from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.config.config import db
from datetime import datetime
from app.models.LiquidSegmentation import segment_image
from app.models.pH_Classification import classify_ph
import cv2
import numpy as np
from google.cloud import storage
import uuid
import os
from google.oauth2 import service_account

# Konfigurasi Google Cloud Storage
GCS_BUCKET_NAME = "ph-app-v1-bucket"  # Ganti dengan nama bucket Anda
GCS_BASE_URL = f"https://storage.googleapis.com/{GCS_BUCKET_NAME}/"

# Menentukan path absolut ke file kredensial
KEY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config", "gcsKey.json")

def upload_image_to_gcs(image_data, filename, content_type):
    """Mengunggah file ke Google Cloud Storage dan mengembalikan URL publiknya."""
    try:
        # Membaca kredensial dari file dan membuat client Storage
        credentials = service_account.Credentials.from_service_account_file(KEY_PATH)

        # Inisialisasi klien GCS dengan kredensial
        storage_client = storage.Client(credentials=credentials, project=credentials.project_id)
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

        # Baca data binari gambar agar bisa digunakan dua kali
        image_data = image_file.read()

        # Generate nama file unik dalam folder user di GCS
        file_extension = image_file.filename.rsplit('.', 1)[-1].lower()
        filename = f"user/{userId}/{uuid.uuid4().hex}.{file_extension}"

        # Upload gambar ke GCS
        image_url = upload_image_to_gcs(image_data, filename, image_file.mimetype)

        # Load image ke dalam numpy array untuk diproses
        np_img = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        # Segmentasi gambar
        segmented_image = segment_image(image)
        if segmented_image is None:
            return jsonify({"error": "Segmentation failed or no liquid detected."}), 400

        # Klasifikasi nilai pH
        predicted_ph = classify_ph(segmented_image)

        # Generate unique history ID
        user_ref = db.collection('user').document(userId)
        history_ref = user_ref.collection('history')
        history_count = len(history_ref.get())
        history_id = f"h{history_count + 1:03d}"

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
            "tanggal": datetime.now().strftime("%d/%m/%Y"),
            "urlGambar": image_url
        }
        return jsonify(response), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
