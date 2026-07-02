from ultralytics import YOLO
import cv2
import winsound
import time
from datetime import datetime
import os

# ===========================
# MODEL
# ===========================
model = YOLO("runs/detect/fire_smoke_v4/weights/best.pt")
# ===========================
# KAMERA
# ===========================
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Kamera açılamadı!")
    exit()

# ===========================
# AYARLAR
# ===========================
last_alarm = 0
alarm_delay = 5

danger_frames = 0
required_frames = 3

prev_time = time.time()

os.makedirs("detections", exist_ok=True)

last_save = 0
save_delay = 5
fire_total = 0
smoke_total = 0

log_file = "log.txt"

# ===========================
# ANA DÖNGÜ
# ===========================
while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = model.predict(
        frame,
        conf=0.60,
        verbose=False
    )

    annotated = frame.copy()

    # ===========================
    # FPS
    # ===========================
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    # ===========================
    # TARİH SAAT
    # ===========================
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    cv2.putText(
        annotated,
        now,
        (330,25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255,255,255),
        2
    )

    cv2.putText(
        annotated,
        f"FPS: {int(fps)}",
        (330,330),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0,255,255),
        2
    )

    danger = False
    fire_count = 0
    smoke_count = 0

    # ===========================
    # TESPİTLER
    # ===========================
    for box in results[0].boxes:

        conf = float(box.conf[0])
        if conf < 0.60:
            continue

        cls = int(box.cls[0])
        label = model.names[cls]

        x1,y1,x2,y2 = map(int, box.xyxy[0])

        color = (0,0,255) if label=="fire" else (0,255,255)

        cv2.rectangle(annotated,(x1,y1),(x2,y2),color,2)
        cv2.putText(
            annotated,
            f"{label} {conf:.2f}",
            (x1,max(20,y1-10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

        if label == "fire":
            fire_count += 1
            fire_total += 1
            danger = True

        elif label == "smoke":
            smoke_count += 1
            smoke_total += 1
            danger = True
    # ===========================
    # TEHLİKE VAR
    # ===========================
    if danger:
        danger_frames += 1
    else:
        danger_frames = 0

    if danger_frames >= required_frames:

        # Kırmızı LED
        cv2.circle(annotated, (600, 40), 15, (0, 0, 255), -1)

        cv2.rectangle(annotated, (0, 0), (640, 80), (0, 0, 255), -1)
        

        cv2.putText(
            annotated,
            "YANGIN / DUMAN TESPIT EDILDI!",
            (20,35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255,255,255),
            2
        )

        cv2.putText(
            annotated,
            f"Fire: {fire_count}   Smoke: {smoke_count}",
            (20,70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255,255,255),
            2
        )

        # Alarm
        if time.time() - last_alarm > alarm_delay:

            winsound.Beep(1800,700)

            last_alarm = time.time()
            
        with open(log_file, "a", encoding="utf-8") as log:
         log.write(
            f"{datetime.now().strftime('%d.%m.%Y %H:%M:%S')} | Fire={fire_count} | Smoke={smoke_count}\n"
        )

        # Fotoğraf Kaydet
        if time.time() - last_save > save_delay:

            filename = datetime.now().strftime(
                "detections/fire_%Y%m%d_%H%M%S.jpg"
            )

            cv2.imwrite(filename, annotated)

            print("Kaydedildi:", filename)

            last_save = time.time()

    # ===========================
    # GÜVENLİ
    # ===========================
    else:

        # Yeşil LED
        cv2.circle(annotated, (600, 40), 15, (0, 255, 0), -1)

        cv2.rectangle(
            annotated,
            (0, 0),
            (420, 60),
            (0, 180, 0),
            -1
        )

        cv2.putText(
            annotated,
            "SYSTEM SAFE",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255,255,255),
            2
        )

    # ===========================
    # GÖSTER
    # ===========================
    cv2.imshow(
        "Fire Detection System",
        annotated
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# ===========================
# ÇIKIŞ
# ===========================
cap.release()
cv2.destroyAllWindows()