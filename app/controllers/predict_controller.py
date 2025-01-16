from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from uuid import uuid4
from google.cloud import storage
from app.config.config import db
from datetime import datetime

# Inisialisasi Cloud Storage
storage_client = storage.Client()
bucket_name = "your-cloud-storage-bucket-name"
bucket = storage_client.bucket(bucket_name)

def predict():
    try:
        # Ekstrak userId dari token JWT
        userId = get_jwt_identity()

        # Validasi request body
        if 'name' not in request.form or 'description' not in request.form or 'image' not in request.files:
            return jsonify({"error": "Invalid input. 'name', 'description', and 'image' are required."}), 400

        name = request.form['name']
        description = request.form['description']
        image_file = request.files['image']

        # Validasi tipe file
        if not image_file.mimetype in ['image/jpeg', 'image/png']:
            return jsonify({"error": "Invalid file type. Only JPG, JPEG, and PNG are allowed."}), 400

        # Generate unique file name untuk diunggah
        file_extension = image_file.filename.rsplit('.', 1)[-1].lower()
        unique_filename = f"{uuid4()}.{file_extension}"

        # Unggah gambar ke Cloud Storage
        blob = bucket.blob(f"history/{userId}/{unique_filename}")
        blob.upload_from_file(image_file, content_type=image_file.mimetype)
        blob.make_public()

        # URL gambar di Cloud Storage
        image_url = blob.public_url

        # Simpan data ke subcollection 'history'
        user_ref = db.collection('user').document(userId)
        history_ref = user_ref.collection('history')
        history_ref.add({
            "name": name,
            "description": description,
            "image_url": image_url,
            "timestamp": datetime.now()
        })

        # Respons
        response = {
            "name": name,
            "description": description,
            "image_url": image_url
        }
        return jsonify(response), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
