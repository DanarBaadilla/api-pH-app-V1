from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.config.config import db
from datetime import datetime
from app.models.LiquidSegmentation import segment_image
from app.models.pH_Classification import classify_ph
import cv2
import numpy as np

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

        # Load image into numpy array
        np_img = np.frombuffer(image_file.read(), np.uint8)
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

        # Simpan data ke database
        history_ref.document(history_id).set({
            "name": name,
            "description": description,
            "historyId": history_id,
            "pH": predicted_ph,
            "timestamp": datetime.now().strftime("%d/%m/%Y")
        })

        # Respons
        response = {
            "name": name,
            "description": description,
            "historyId": history_id,
            "pH": predicted_ph,
            "timestamp": datetime.now().strftime("%d/%m/%Y")
        }
        return jsonify(response), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
