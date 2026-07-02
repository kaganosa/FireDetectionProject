from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO("yolov8s.pt")

    model.train(
        data=r"C:\Users\ASUS\OneDrive\Desktop\FireDetectionProjesi\data.yaml",
        epochs=200,
        imgsz=640,
        device=0,
        workers=0,
        cls=1.5,
        dropout=0.1,
        patience=25,
        degrees=10.0,
        fliplr=0.5,
        flipud=0.1,
        mosaic=1.0,
        mixup=0.1,
        hsv_h=0.015,
        hsv_s=0.5,
        hsv_v=0.4,
        save=True,
        save_period=10,
        name="fire_smoke_v2",
        exist_ok=True,
    )

    print("\n✅ Eğitim tamamlandı!")
    print("📁 En iyi model: runs/detect/fire_smoke_v2/weights/best.pt")