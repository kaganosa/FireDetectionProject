import cv2
import os

videos = [f for f in os.listdir() if f.startswith("ateşvideo") and f.endswith(".mp4")]

output_folder = "fire_images"
os.makedirs(output_folder, exist_ok=True)

saved = 0

for video in videos:

    print(f"İşleniyor: {video}")

    cap = cv2.VideoCapture(video)
    count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if count % 10 == 0:

            filename = os.path.join(
                output_folder,
                f"fire_{saved:04d}.jpg"
            )

            cv2.imwrite(filename, frame)

            saved += 1

        count += 1

    cap.release()

print(f"\nToplam {saved} adet fire görüntüsü kaydedildi.")