import os
import shutil
import random

# Görüntü ve etiket dizinlerinin yolu
image_dir = r"C:\Users\yusuf\PycharmProjects\licenseplate12\plakalar\images"
label_dir = r"C:\Users\yusuf\PycharmProjects\licenseplate12\plakalar\labels"

# Eğitim ve doğrulama için yeni dizinler
train_image_dir = r"C:\Users\yusuf\PycharmProjects\licenseplate12\dataset\images\train"
val_image_dir = r"C:\Users\yusuf\PycharmProjects\licenseplate12\dataset\images\val"
train_label_dir = r"C:\Users\yusuf\PycharmProjects\licenseplate12\dataset\labels\train"
val_label_dir = r"C:\Users\yusuf\PycharmProjects\licenseplate12\dataset\labels\val"

# Yeni dizinleri oluştur
os.makedirs(train_image_dir, exist_ok=True)
os.makedirs(val_image_dir, exist_ok=True)
os.makedirs(train_label_dir, exist_ok=True)
os.makedirs(val_label_dir, exist_ok=True)

# Tüm görüntü dosyalarını al
image_files = [f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Eğitim seti için yüzde oranı
train_ratio = 0.8
train_size = int(len(image_files) * train_ratio)

# Dosyaları karıştır ve eğitim ve doğrulama setine böl
random.shuffle(image_files)
train_files = image_files[:train_size]
val_files = image_files[train_size:]

# Dosyaları uygun dizinlere taşı
def move_files(files, source_image_dir, source_label_dir, target_image_dir, target_label_dir):
    for file_name in files:
        # Görüntü dosyasını taşı
        src_image_path = os.path.join(source_image_dir, file_name)
        dst_image_path = os.path.join(target_image_dir, file_name)
        shutil.move(src_image_path, dst_image_path)

        # Aynı isimdeki etiket dosyasını taşı
        label_file = file_name.replace(".jpg", ".txt").replace(".png", ".txt")
        src_label_path = os.path.join(source_label_dir, label_file)
        dst_label_path = os.path.join(target_label_dir, label_file)

        if os.path.exists(src_label_path):
            shutil.move(src_label_path, dst_label_path)

# Eğitim ve doğrulama setine dosyaları taşı
move_files(train_files, image_dir, label_dir, train_image_dir, train_label_dir)
move_files(val_files, image_dir, label_dir, val_image_dir, val_label_dir)

print("Veri seti başarıyla ayrıldı!")
