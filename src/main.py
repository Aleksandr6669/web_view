import flet as ft
import os

def main(page: ft.Page):
    page.title = "Камера в WebView"

    # Путь к HTML-файлу с камерой
    html_file_path = os.path.join(os.path.dirname(__file__), "camera_extension", "camera.html")

    # Чтение HTML-файла
    with open(html_file_path, "r", encoding="utf-8") as file:
        camera_html = file.read()

    # Добавляем WebView для отображения камеры
    page.add(ft.WebView(content=camera_html))

# Запускаем приложение
ft.app(target=main)