import flet as ft
import os

def main(page: ft.Page):
    page.title = "Видеоискатель в браузере"

    # Проверяем, существует ли HTML-файл
    html_path = os.path.abspath("camera.html")
    if not os.path.exists(html_path):
        page.add(ft.Text("Ошибка: файл camera.html не найден!", color="red"))
        return

    # WebView для загрузки камеры
    web_view = ft.WebView(url=f"file://{html_path}")

    page.add(ft.Text("Видео с камеры"))
    page.add(web_view)

ft.app(target=main, view=ft.WEB_BROWSER)  # Запускаем Flet в браузере