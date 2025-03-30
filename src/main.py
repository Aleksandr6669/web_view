import flet as ft

def main(page: ft.Page):
    # Заголовок
    page.add(ft.Text("Видеокамера с возможностью захвата изображения", size=30, color=ft.colors.BLACK))

    # Встраиваем библиотеку JS
    page.add(ft.Html(
        content="""
        <script src="camera.js"></script>
        <video id="video" width="640" height="480" autoplay></video>
        <canvas id="canvas" width="640" height="480" style="display:none;"></canvas>
        <button onclick="captureImage()">Захватить изображение</button>
        <script>
            // Инициализация камеры с помощью библиотеки
            let captureImage = Camera.init('video', 'canvas', function(imageData) {
                window.flutter_inappwebview.callHandler('imageCaptured', imageData);
            });
        </script>
        """
    ))

    # Контейнер для отображения захваченного изображения
    captured_image = ft.Image(src="", width=640, height=480)
    page.add(captured_image)

    # Обработчик вызова JavaScript из Flet
    def handle_image_capture(image_data):
        captured_image.src = image_data
        page.update()

    # Регистрация обработчика для JS
    page.add(ft.JsHandler("imageCaptured", handle_image_capture))

ft.app(target=main)
