import cv2
import numpy as np
from keras.models import load_model

# Load pre-trained model
model = load_model('app/models/TrainedModel/CNN_pH_Classification.h5')
class_list = ["10", "11", "12", "13", "2", "3", "4", "5", "6", "7", "8", "9"]

def classify_ph(image):
    """
    Melakukan klasifikasi nilai pH berdasarkan gambar input.
    Args:
        image: Gambar input dalam format numpy array (BGR).

    Returns:
        predicted_ph: String nilai pH yang diprediksi.
    """
    img_resized = cv2.resize(image, (64, 64))
    img_resized = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
    img_resized = img_resized.astype(np.float32) / 255.0
    img_resized = np.expand_dims(img_resized, axis=0)

    prediction = model.predict(img_resized)
    predicted_class_idx = np.argmax(prediction)
    predicted_ph = class_list[predicted_class_idx]
    return predicted_ph
