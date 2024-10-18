import torch
import cv2
import pytesseract
import os
from datetime import datetime

# YOLOv5 modelini yükle
model = torch.hub.load('ultralytics/yolov5', 'custom', path=r'C:\Users\yusuf\PycharmProjects\licenseplate12\yolov5\runs\train\plate_detection\weights\best.pt')

# Log dosyası için klasör
log_dir = r"C:\Users\yusuf\PycharmProjects\licenseplate12\log"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# OCR için Tesseract yapılandırması
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Tesseract'in kurulu olduğu yol


def plaka_tespiti(image_path):
    # YOLOv5 ile plaka tespiti yap
    results = model(image_path)

    # Tespit edilen plakaların koordinatlarını al
    detections = results.xyxy[0].cpu().numpy()  # Koordinatlar: [xmin, ymin, xmax, ymax, confidence, class]

    # Görüntüyü aç
    img = cv2.imread(image_path)

    # Her bir plakayı OCR ile okumak için döngü
    plaka_sonuclari = []
    for detection in detections:
        xmin, ymin, xmax, ymax, confidence, cls = detection
        if confidence >= 0.25:  # Güven aralığı filtresi
            # Plaka bölgesini kırp
            plaka_resmi = img[int(ymin):int(ymax), int(xmin):int(xmax)]

            # OCR ile plaka okuma
            plaka_text = pytesseract.image_to_string(plaka_resmi, config='--psm 8')

            # Plakanın başındaki ilk karakteri kaldırma
            temiz_plaka = plaka_text[1:].strip()  # İlk karakteri atla

            plaka_sonuclari.append({
                "plaka": temiz_plaka,
                "koordinatlar": (xmin, ymin, xmax, ymax),
                "guvenlik": confidence
            })

    return plaka_sonuclari


def log_kaydet(image_path, plaka_sonuclari):
    # Log dosyasına tespit edilen plakaları yaz
    log_file_path = os.path.join(log_dir, "plaka_tespit_log.txt")

    with open(log_file_path, "a") as log_file:
        log_file.write(f"Tarih: {datetime.now()}\n")
        log_file.write(f"Görüntü: {image_path}\n")
        for entry in plaka_sonuclari:
            log_file.write(
                f"Plaka: {entry['plaka']}, Koordinatlar: {entry['koordinatlar']}, Güvenlik: {entry['guvenlik']:.2f}\n")
        log_file.write("\n")


# Test etmek için bir görüntü üzerinde çalışalım
image_path = r"C:\Users\yusuf\PycharmProjects\licenseplate12\test\1.jpg"  # Test edilecek görüntü yolu
plaka_sonuclari = plaka_tespiti(image_path)
log_kaydet(image_path, plaka_sonuclari)

print(f"{len(plaka_sonuclari)} plaka bulundu ve log'a kaydedildi.")
