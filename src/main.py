import flet as ft

def main(page: ft.Page):
    page.title = "Видеокамера в Flet (JS)"

    # Контейнер для отображения захваченного изображения
    captured_image = ft.Image(src="", width=640, height=480)

    def handle_image_capture(image_data):
        """Получаем изображение из JavaScript и показываем в Flet"""
        captured_image.src = image_data
        page.update()

    # Встроенный JavaScript-код для работы с камерой
    camera_js = """
    <script>
        let video;
        let canvas;
        let context;

        function initCamera() {
            video = document.createElement("video");
            video.width = 640;
            video.height = 480;
            document.body.appendChild(video);

            canvas = document.createElement("canvas");
            canvas.width = 640;
            canvas.height = 480;
            context = canvas.getContext("2d");

            if (navigator.mediaDevices.getUserMedia) {
                navigator.mediaDevices.getUserMedia({ video: true })
                    .then(function(stream) {
                        video.srcObject = stream;
                        video.play();
                    })
                    .catch(function(error) {
                        alert("Ошибка при доступе к камере: " + error);
                    });
            }
        }

        function captureImage() {
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            let imageData = canvas.toDataURL("image/png");
            window.flutter_inappwebview.callHandler("imageCaptured", imageData);
        }

        window.onload = function() {
            initCamera();
            let button = document.createElement("button");
            button.innerText = "Захватить изображение";
            button.onclick = captureImage;
            document.body.appendChild(button);
        }
    </script>
    """

    # WebView с JavaScript-кодом
    web_view = ft.WebView(
        html=f"<html><body>{camera_js}</body></html>",
        on_message=handle_image_capture,
    )

    page.add(ft.Text("Камера в Flet на чистом JS"))
    page.add(web_view)
    page.add(captured_image)

ft.app(target=main)