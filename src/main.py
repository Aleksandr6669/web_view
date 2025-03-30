import flet as ft
import cv2

def main(page: ft.Page):
    def capture_camera(e):
        cap = cv2.VideoCapture(0)  # Открываем доступ к камере
        ret, frame = cap.read()  # Считываем один кадр
        if ret:
            cv2.imwrite("snapshot.png", frame)  # Сохраняем снимок в файл
            page.add(ft.Text("Снимок сохранён как 'snapshot.png'."))
        else:
            page.add(ft.Text("Не удалось сделать снимок."))
        cap.release()

    page.title = "Камера на Flet"
    page.add(ft.TextButton("Сделать снимок", on_click=capture_camera))

ft.app(target=main)