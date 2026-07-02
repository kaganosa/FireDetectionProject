# Fire & Smoke Detection System (YOLOv8)

Bu proje, Mersin Üniversitesi Bilişim Sistemleri ve Teknolojileri Bölümü kapsamında geliştirilmiş, YOLOv8 tabanlı gerçek zamanlı yangın ve duman tespit sistemidir.

Sistem; fotoğraf analizi ve canlı kamera üzerinden yangın ile duman tespiti gerçekleştirebilmektedir.

---

# Proje Özellikleri

- Yangın (Fire) tespiti
- Duman (Smoke) tespiti
- Gerçek zamanlı kamera desteği
- Fotoğraf yükleyerek analiz
- Confidence ve IOU eşik değerlerinin ayarlanabilmesi
- Streamlit tabanlı kullanıcı arayüzü
- Alarm sistemi
- Tespit edilen görüntülerin kaydedilmesi
- Log kaydı oluşturulması

---

# Kullanılan Teknolojiler

- Python
- YOLOv8 (Ultralytics)
- PyTorch
- OpenCV
- Streamlit
- NumPy
- Pillow

---

# Proje Yapısı

```
FireDetection/

│── demo_app.py
│── alarm_app_final.py
│── best.pt
│── requirements.txt
│── README.md
│── data.yaml
│── test.jpg
```

---

# Kurulum

Projeyi bilgisayarınıza klonlayın.

```bash
git clone https://github.com/KULLANICI_ADIN/FireDetection.git
```

Proje klasörüne girin.

```bash
cd FireDetection
```

Gerekli kütüphaneleri yükleyin.

```bash
pip install -r requirements.txt
```

---

# Çalıştırma

Uygulamayı başlatmak için aşağıdaki komutu çalıştırın.

```bash
streamlit run demo_app.py
```

Ardından uygulama tarayıcı üzerinden açılacaktır.

---

# Kullanım

## Fotoğraf Analizi

- Bir görüntü yükleyin.
- Model görüntüyü analiz eder.
- Yangın veya duman tespit edilirse sonuç ekranda gösterilir.

## Canlı Kamera

- Canlı kamera modunu seçin.
- Kamera görüntüsü gerçek zamanlı olarak analiz edilir.
- Yangın veya duman tespit edildiğinde alarm sistemi devreye girer.

---

# Model Bilgileri

Model, YOLOv8 kullanılarak eğitilmiştir.

Sınıflar:

- Fire
- Smoke

Model dosyası:

```
best.pt
```

---

# Performans Değerlendirmesi

Model performansı aşağıdaki metrikler kullanılarak değerlendirilmiştir.

- Precision
- Recall
- F1 Score
- Precision-Recall Curve
- Confusion Matrix

---

# Geliştirici

Taha Kağan Aşğa

Mersin Üniversitesi

Bilişim Sistemleri ve Teknolojileri

2026

---

# Lisans

Bu proje eğitim amaçlı geliştirilmiştir.
