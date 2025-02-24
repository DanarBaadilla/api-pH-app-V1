import cv2
import numpy as np
import tensorflow as tf

# Load model CNN yang sudah diperbarui
model = tf.keras.models.load_model('app/models/TrainedModel/best_CNN_pH_prediciton_model_valACC92.h5')

# Daftar label kelas (pH values)
class_list = ['10', '11', '12', '13', '2', '3', '4', '5', '6', '7', '8', '9']

# Definisikan parameter normalisasi sesuai dataset training
dataset_mean = np.array([0.2757323, 0.28446444, 0.33513261], dtype=np.float32)
dataset_std = np.array([0.21059035, 0.2042752, 0.22735262], dtype=np.float32)

def preprocess_image(img_array, target_size=(227, 227)):
    """
    Fungsi untuk memproses gambar sebelum diberikan ke model CNN.
    - Mengubah ukuran gambar
    - Menormalisasi dengan mean dan std dataset training
    - Mengubah ke format batch (1, height, width, channels)
    
    Args:
        img_array (numpy array): Gambar dalam format array (OpenCV BGR format)
        target_size (tuple): Ukuran target gambar (default: 227x227)
    
    Returns:
        np.array: Gambar yang telah diproses dan siap diberikan ke model CNN
    """
    # Konversi dari BGR (OpenCV) ke RGB
    img_rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

    # Resize gambar ke ukuran yang dibutuhkan model
    img_resized = cv2.resize(img_rgb, target_size)

    # Ubah tipe data ke float32 dan normalisasi ke [0,1]
    img_resized = img_resized.astype(np.float32) / 255.0

    # Normalisasi menggunakan mean dan std dari dataset training
    img_normalized = (img_resized - dataset_mean) / dataset_std

    # Tambahkan dimensi batch (1, height, width, channels) agar sesuai input model
    img_batch = np.expand_dims(img_normalized, axis=0)

    return img_batch

def classify_ph(image_array):
    """
    Fungsi untuk melakukan klasifikasi nilai pH menggunakan model CNN terbaru.
    
    Args:
        image_array (numpy array): Gambar dalam format array (OpenCV BGR format)
    
    Returns:
        str: Prediksi nilai pH
    """
    # Lakukan preprocessing gambar sebelum diberikan ke model
    img_input = preprocess_image(image_array)

    # Lakukan inferensi dengan model CNN
    predictions = model.predict(img_input)

    # Ambil indeks kelas dengan probabilitas tertinggi
    predicted_class_idx = np.argmax(predictions)

    # Ambil nilai pH yang sesuai dengan indeks tersebut
    predicted_ph = class_list[predicted_class_idx]

    return predicted_ph
