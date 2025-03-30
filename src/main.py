import flet as ft
import base64

def main(page: ft.Page):
    page.title = "Открытие фото в Flet"

    # Функция обработки выбора файла
    def pick_result(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path  # Получаем путь к файлу
            with open(file_path, "rb") as image_file:
                img.src_base64 = base64.b64encode(image_file.read()).decode("utf-8")
            page.update()

    # Создаём FilePicker
    file_picker = ft.FilePicker(on_result=pick_result)
    page.overlay.append(file_picker)

    # Кнопка для выбора изображения
    open_btn = ft.ElevatedButton(
        text="Выбрать фото",
        on_click=lambda e: file_picker.pick_files(
            allow_multiple=False, allowed_extensions=["png", "jpg", "jpeg"]
        )
    )

    # Контейнер для изображения
    img = ft.Image(width=400, height=400, fit=ft.ImageFit.CONTAIN)

    page.add(open_btn, img)

ft.app(target=main)