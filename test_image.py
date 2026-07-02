from ultralytics import YOLO

model = YOLO("runs/detect/fire_smoke_v4/weights/best.pt")

results = model.predict(
    source="test.jpg",
    imgsz=1280,
    conf=0.10,
    save=True
)

print(results)