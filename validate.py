from ultralytics import YOLO

model = YOLO("best.pt")

metrics = model.val(
    data="data.yaml",
    split="test",
    imgsz=640,
    save_json=True,
    plots=True
)

print(metrics)