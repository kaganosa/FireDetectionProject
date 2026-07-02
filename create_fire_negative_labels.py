import os

images_dir = "train/images"
labels_dir = "train/labels"

count = 0

for filename in os.listdir(images_dir):
    if filename.startswith("fire") and filename.lower().endswith((".jpg", ".jpeg", ".png")):
        label_name = os.path.splitext(filename)[0] + ".txt"
        label_path = os.path.join(labels_dir, label_name)

        if not os.path.exists(label_path):
            open(label_path, "w").close()
            count += 1

print(f"{count} adet negatif label oluşturuldu.")