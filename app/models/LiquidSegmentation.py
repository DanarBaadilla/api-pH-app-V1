import torch
import numpy as np
#import PSPNet_Architecture as PSPNet  # Class Arsitektur Model
from app.models import PSPNet_Architecture as PSPNet
#import CategoryDictionary as CatDic
from app.models import CategoryDictionary as CatDic
import cv2

# Path model PSPNet
Trained_model_path = "app/models/TrainedModel/PSPNet_Semantic_Segmentation.torch"

# Inisialisasi model PSPNet
UseGPU = False  # Gunakan CPU secara default
FreezeBatchNormStatistics = True  # Freeze statistik batch normalisasi untuk inferensi

Net = PSPNet.Net(CatDic.CatNum)
if UseGPU:
    print("USING GPU")
    Net.load_state_dict(torch.load(Trained_model_path))
else:
    print("USING CPU")
    Net.load_state_dict(torch.load(Trained_model_path, map_location=torch.device("cpu")))

# Fungsi untuk mendapatkan mask terbesar
def get_largest_mask(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return None  # Tidak ada kontur ditemukan
    largest_contour = max(contours, key=cv2.contourArea)
    largest_mask = np.zeros_like(mask)
    cv2.drawContours(largest_mask, [largest_contour], -1, 255, thickness=cv2.FILLED)
    return largest_mask, largest_contour

# Fungsi segmentasi gambar
def segment_image(image):
    try:
        # Resize jika gambar lebih besar dari 840x840
        h, w, d = image.shape
        max_size = max(h, w)
        if max_size > 840:
            resize_factor = 840 / max_size
            image = cv2.resize(image, (int(w * resize_factor), int(h * resize_factor)))

        # Konversi ke batch untuk model
        image_batch = np.expand_dims(image, axis=0)

        # Inferensi PSPNet
        with torch.no_grad():
            _, OutLbDict = Net.forward(
                Images=image_batch,
                TrainMode=False,
                UseGPU=UseGPU,
                FreezeBatchNormStatistics=FreezeBatchNormStatistics,
            )

        # Ambil mask untuk kategori "Liquid GENERAL"
        category_name = "Liquid GENERAL"
        if category_name in OutLbDict:
            mask = OutLbDict[category_name].data.cpu().numpy()[0].astype(np.uint8)
            if mask.mean() > 0.001:
                largest_mask, largest_contour = get_largest_mask(mask)
                if largest_mask is not None:
                    # Ambil bounding box dan crop gambar
                    x, y, w, h = cv2.boundingRect(largest_contour)
                    cropped_image = image[y : y + h, x : x + w]
                    cropped_mask = largest_mask[y : y + h, x : x + w]

                    # Segmentasi objek berdasarkan mask
                    segmented_object = cv2.bitwise_and(
                        cropped_image, cropped_image, mask=cropped_mask
                    )
                    return segmented_object
        return None
    except Exception as e:
        print(f"Error during segmentation: {e}")
        return None
