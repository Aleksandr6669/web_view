import flet as ft
import base64
import os

def main(page: ft.Page):
    page.title = "Галерея | Открытие фото"
    page.bgcolor = ft.colors.GREY_200  # Фон приложения
    page.padding = 20

    # Заголовок
    title = ft.Text("Выберите изображение", size=24, weight=ft.FontWeight.BOLD, text_align="center")

    # Заглушка, если фото нет
    placeholder = ft.Text("Нет изображения", size=18, italic=True, color=ft.colors.GREY)

    # Виджет изображения (по умолчанию скрыт)
    img = ft.Image(width=400, height=400, fit=ft.ImageFit.CONTAIN, visible=False)

    # Функция обработки выбора файла
    def pick_result(e: ft.FilePickerResultEvent):
        if e.files and e.files[0].path:
            file_path = e.files[0].path  # Путь к файлу
            
            if not os.path.exists(file_path):  # Проверка на существование файла
                return
            
            with open(file_path, "rb") as image_file:
                img.src_base64 = base64.b64encode(image_file.read()).decode("utf-8")
            
            img.visible = True  # Показываем изображение
            placeholder.visible = False  # Скрываем заглушку
        else:
            img.visible = False
            placeholder.visible = True
        
        page.update()

    # Создаём FilePicker
    file_picker = ft.FilePicker(on_result=pick_result)
    page.overlay.append(file_picker)

    # Кнопка для выбора изображения
    open_btn = ft.ElevatedButton(
        text="Выбрать фото 📷",
        icon=ft.icons.IMAGE,
        bgcolor=ft.colors.BLUE,
        color=ft.colors.WHITE,
        on_click=lambda e: file_picker.pick_files(
            allow_multiple=False, allowed_extensions=["png", "jpg", "jpeg"]
        )
    )

    # Компоновка
    page.add(
        ft.Column(
            [
                title,
                open_btn,
                placeholder,  # Текст "Нет изображения"
                img  # Картинка
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

ft.app(target=main)