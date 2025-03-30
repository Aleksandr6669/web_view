import flet as ft
import flet_camera as fc

def main(page: ft.Page):
    # Попробуем проверить доступность камеры через flet-camera
    camera_view = fc.CameraView(on_capture=lambda image: print(f"Изображение: {image}"))
    page.add(camera_view)

ft.app(target=main)