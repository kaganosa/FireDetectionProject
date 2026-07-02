import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import subprocess
import sys
import os

from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
import av
import cv2
import os
from datetime import datetime

st.set_page_config(
    page_title="Yangın ve Duman Algılama Sistemi",
    page_icon="🔥",
    layout="wide"
)

st.title("🔥 Yangın ve Duman Algılama Sistemi")
st.markdown("### YOLOv8 Tabanlı Fire & Smoke Detection")

# ===========================
# MODEL
# ===========================
@st.cache_resource
def load_demo_model():
    return YOLO("best.pt")

model = load_demo_model()

rtc_configuration = RTCConfiguration(
    {
        "iceServers": [
            {"urls": ["stun:stun.l.google.com:19302"]}
        ]
    }
)

os.makedirs("detections", exist_ok=True)

class VideoProcessor(VideoProcessorBase):

    def recv(self, frame):

        img = frame.to_ndarray(format="bgr24")

        conf = st.session_state.get("conf", 0.60)
        iou = st.session_state.get("iou", 0.45)

        results = model.predict(
            img,
            conf=conf,
            iou=iou,
            verbose=False
        )

        annotated = results[0].plot()

        return av.VideoFrame.from_ndarray(
            annotated,
            format="bgr24"
        )
# ===========================
# SIDEBAR
# ===========================
st.sidebar.header("⚙️ Sistem Ayarları")

mode = st.sidebar.radio(
    "Çalışma Modu",
    [
        "🖼️ Fotoğraf Analizi",
        "📷 Canlı Kamera (Alarm Sistemi)"
    ]
)

confidence_threshold = st.sidebar.slider(
    "Confidence",
    0.05,
    0.95,
    0.60,
    0.05
    

)

iou_threshold = st.sidebar.slider(
    "IOU",
    0.10,
    0.90,
    0.45,
    0.05
    
)

st.sidebar.markdown("---")
st.sidebar.success("Model : fire_smoke_v4")


# ===========================
# CANLI KAMERA
# ===========================
if mode == "📷 Canlı Kamera (Alarm Sistemi)":

    st.header("📷 Canlı Kamera")

    st.write(
        """
Bu butona bastığınızda alarm sistemi açılır.

Özellikler:

- Yangın Algılama
- Duman Algılama
- Sesli Alarm
- Log Kaydı
- Detections Kaydı
- 3 Kare Doğrulama
- 5 Saniye Alarm Gecikmesi
"""
    )

    if st.button("🎥 Kamerayı Başlat"):

        subprocess.Popen(
            [sys.executable, "alarm_app_final.py"]
        )

        st.success("Alarm sistemi başlatıldı.")

    st.stop()

# ===========================
# FOTOĞRAF ANALİZİ
# ===========================

st.header("🖼️ Fotoğraf Analizi")

# ==========================
# CANLI KAMERA
# ==========================



uploaded_file = st.file_uploader(
    "Fotoğraf Seçiniz",
    type=["jpg","jpeg","png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Orijinal Görüntü")

        st.image(
            image,
            use_container_width=True
        )

    with col2:

        st.subheader("Model Sonucu")

        img_array = np.array(image)

        results = model.predict(
            img_array,
            conf=confidence_threshold,
            iou=iou_threshold
        )

        annotated = results[0].plot()

        st.image(
            annotated,
            use_container_width=True
        )

    st.markdown("---")

    st.subheader("📋 Tespit Raporu")

    boxes = results[0].boxes

    if len(boxes):

        fire_count = 0
        smoke_count = 0

        for box in boxes:

            cls = int(box.cls[0])

            if model.names[cls] == "fire":
                fire_count += 1

            if model.names[cls] == "smoke":
                smoke_count += 1

        if fire_count:

            st.error(
                f"🔥 {fire_count} adet FIRE tespit edildi."
            )

        if smoke_count:

            st.warning(
                f"💨 {smoke_count} adet SMOKE tespit edildi."
            )

        st.markdown("### Detaylar")

        for i, box in enumerate(boxes):

            cls = int(box.cls[0])

            label = model.names[cls]

            conf = float(box.conf[0])

            if label == "fire":

                st.error(
                    f"{i+1}. FIRE | Confidence : %{conf*100:.2f}"
                )

            else:

                st.warning(
                    f"{i+1}. SMOKE | Confidence : %{conf*100:.2f}"
                )

    else:

        st.success(
            "✅ Herhangi bir yangın veya duman tespit edilmedi."
        )