from flask import jsonify
from app.config.config import db

def get_tutorial():
    # Query ke Firestore untuk mendapatkan data tutorial
    tutorial_ref = db.collection('tutorials')
    results = tutorial_ref.stream()

    # list untuk menyimpan data tutorial
    tutorials_data = []

    for result in results:
        tutorial_data = result.to_dict()
        tutorials_data.append(tutorial_data)

    # return response json  
    response = {"tutorials": tutorials_data}
    return jsonify(response), 200