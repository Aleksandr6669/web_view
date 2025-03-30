import flet as ft
import os

def main(page: ft.Page):
    page.title = "Приложение с камерой"

    # Путь к HTML-файлу с камерой
    html_file_path = os.path.join(os.path.dirname(__file__), "camera_extension", "camera.html")

    # Добавляем WebView для отображения камеры
    page.add(ft.WebView(url=f"file://{html_file_path}"))

# Запуск приложения Flet
ft.app(target=main)