import numpy as np
from keras._tf_keras.keras.models import load_model
import tensorflow as tf

#Lambda Layer Function Definition
def slice_first_24(x):
    return x[:, :, :, :24]

def slice_last_24(x):
    return x[:, :, :, 24:]

def slice_first_96(x):
    return x[:, :, :, :96]

def slice_last_96(x):
    return x[:, :, :, 96:]

# Load model CNN yang sudah diperbarui
model = load_model(
    'app/models/TrainedModel/best_CNN_pH_prediction_model_valACC9350.h5',
    custom_objects={
        'slice_first_24': slice_first_24,
        'slice_last_24': slice_last_24,
        'slice_first_96': slice_first_96,
        'slice_last_96': slice_last_96
    }
)

# Daftar label kelas (pH values)
class_list = ['10', '11', '12', '13', '2', '3', '4', '5', '6', '7', '8', '9']

# Definisikan parameter normalisasi sesuai dataset
dataset_mean = np.array([0.2757323, 0.28446444, 0.33513261], dtype=np.float32)
dataset_std = np.array([0.21059035, 0.2042752, 0.22735262], dtype=np.float32)

def preprocess_image(segmented_object):

    # Konversi ke tensor dan resize
    segmented_object_tensor = tf.convert_to_tensor(segmented_object, dtype=tf.float32)
    segmented_object_resized = tf.image.resize(segmented_object_tensor, [227, 227])
    # Konversi ke tensor, ubah ke float32, dan normalisasi
    segmented_object_tensor = tf.image.convert_image_dtype(segmented_object_resized, tf.float32)
    segmented_object_normalized = (segmented_object_tensor - dataset_mean) / dataset_std
    # Tambahkan dimensi batch: (1, 227, 227, 3)
    cnn_input = tf.expand_dims(segmented_object_normalized, axis=0)
    cnn_input_np = cnn_input.numpy()

    return cnn_input_np

def classify_ph(cnn_input_np):
    """
    Fungsi untuk melakukan klasifikasi nilai pH menggunakan model CNN terbaru.
    
    Returns:
        str: Prediksi nilai pH
    """
    # Lakukan preprocessing gambar sebelum diberikan ke model
    img_input = preprocess_image(cnn_input_np)

    # Lakukan inferensi dengan model CNNs
    predictions = model.predict(img_input)

    # Ambil indeks kelas dengan probabilitas tertinggi
    predicted_class_idx = np.argmax(predictions)

    # Ambil nilai pH yang sesuai dengan indeks tersebut
    predicted_ph = class_list[predicted_class_idx]
    print("Probabilities:", predictions)
    print("Predicted pH Value:", predicted_ph)

    return predicted_ph
