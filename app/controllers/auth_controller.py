from flask import jsonify
from uuid import uuid4
from app.config.config import db
from datetime import datetime
from app.models.user_token import generate_token

def register_guest():
    # Generate userId menggunakan UUID
    userId = str(uuid4())

    # Generate token untuk userId
    token = generate_token(userId)

    # Data untuk disimpan ke Firestore
    user_firestore_data = {
        'userId': userId,
        'token': token,
        'createdAt': datetime.now()
    }

    # Simpan data ke Firestore
    user_ref = db.collection('user').document(userId)
    user_ref.set(user_firestore_data)

    # Respons JSON tanpa field 'createdAt' & 'userId'
    response_data = {
        'token': user_firestore_data['token']
    }

    return jsonify(response_data), 201  # Mengembalikan status HTTP 201 (Created)
