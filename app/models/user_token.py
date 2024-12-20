import jwt
from datetime import datetime, timedelta
from flask import current_app as app

def generate_token(userId):
    payload = {
        'sub': userId,  # Menyimpan userId sebagai subject
        'exp': datetime.utcnow() + timedelta(days=365)  # Atur waktu kedaluwarsa token
    }
    token = jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')
    return token
