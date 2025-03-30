import flet as ft
import cv2
import threading
import time
import base64
import numpy as np
from io import BytesIO
from PIL import Image

def main(page: ft.Page):
    page.title = "Видеоискатель в Flet"
    
    # Элемент для отображения видеопотока
    video_image = ft.Image(width=640, height=480)

    def update_video():
        """Функция потока для обновления видеопотока"""
        cap = cv2.VideoCapture(0)  # Открываем камеру (0 — первая камера)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Конвертируем кадр в Base64
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # OpenCV использует BGR, меняем на RGB
            pil_img = Image.fromarray(frame)
            buffered = BytesIO()
            pil_img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            # Обновляем изображение в Flet
            video_image.src_base64 = img_str
            page.update()
            
            time.sleep(0.03)  # 30 FPS (пауза между кадрами)
        
        cap.release()

    # Запускаем поток с камерой
    thread = threading.Thread(target=update_video, daemon=True)
    thread.start()

    # Добавляем изображение на страницу
    page.add(video_image)

ft.app(target=main)