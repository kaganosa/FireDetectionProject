import os

images_folder = "train/images"
labels_folder = "train/labels"

os.makedirs(labels_folder, exist_ok=True)

count = 0

for file in os.listdir(images_folder):
    if file.startswith("negative_") and file.lower().endswith((".jpg", ".jpeg", ".png")):

        txt_name = os.path.splitext(file)[0] + ".txt"
        txt_path = os.path.join(labels_folder, txt_name)

        with open(txt_path, "w", encoding="utf-8"):
            pass

        count += 1

print(f"{count} adet boş label oluşturuldu.")
import os

images_dir = "train/images"
labels_dir = "train/labels"

os.makedirs(labels_dir, exist_ok=True)

count = 0

for filename in os.listdir(images_dir):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        label_name = os.path.splitext(filename)[0] + ".txt"
        label_path = os.path.join(labels_dir, label_name)

        if not os.path.exists(label_path):
            open(label_path, "w").close()
            count += 1

print(f"{count} adet boş label oluşturuldu.")