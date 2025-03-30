import flet as ft

def main(page: ft.Page):
    page.title = "Старт"
    
    # Указываем URL загруженного HTML-файла
    page.add(ft.WebView(src="https://tmbot.kivismart.com/webapp_index/353095791"))

ft.app(target=main)