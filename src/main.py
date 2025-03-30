import flet as ft

def main(page: ft.Page):
    page.title = "Открытие фото в Flet"

    # Обработчик выбора файла
    def pick_result(e: ft.FilePickerResultEvent):
        if e.files:
            file = e.files[0]
            # Если файл выбран, показываем его
            img.src_base64 = file.content_base64  # файл передаётся в формате base64
            page.update()

    # Создаём FilePicker и добавляем его в overlay страницы
    file_picker = ft.FilePicker(on_result=pick_result)
    page.overlay.append(file_picker)

    # Кнопка для открытия файлового диалога
    open_btn = ft.ElevatedButton(
        text="Выбрать фото",
        on_click=lambda e: file_picker.pick_files(
            allow_multiple=False, allowed_extensions=["png", "jpg", "jpeg"]
        )
    )

    # Компонент для отображения изображения
    img = ft.Image(width=400, height=400, fit=ft.ImageFit.CONTAIN)

    page.add(open_btn, img)

ft.app(target=main)