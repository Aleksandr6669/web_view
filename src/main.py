import flet as ft

# HTML код для доступа к камере
camera_html = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Камера</title>
</head>
<body>
    <h2>Видеопоток</h2>
    <video id="video" width="640" height="480" autoplay></video>
    <button id="capture">Сделать фото</button>
    <canvas id="canvas" style="display:none;"></canvas>

    <script>
        let video = document.getElementById('video');
        let canvas = document.getElementById('canvas');
        let captureButton = document.getElementById('capture');

        // Доступ к камере
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => { video.srcObject = stream; })
            .catch(err => alert("Ошибка: " + err));

        // Сохранение кадра и отправка в Flet
        captureButton.onclick = function() {
            let ctx = canvas.getContext('2d');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            let imageData = canvas.toDataURL('image/png');
            window.parent.postMessage(imageData, "*"); // Отправляем в Flet
        };
    </script>
</body>
</html>
"""

def main(page: ft.Page):
    page.title = "Камера на Flet"

    def on_message(e: ft.WebViewMessageEvent):
        # Получаем изображение в формате base64
        print("Фото получено:", e.message)  
        img.src_base64 = e.message  # Отображаем снимок
        page.update()

    # Кодируем HTML в data URL
    html_data_url = f"data:text/html;charset=utf-8,{camera_html}"

    # Создаем WebView с встроенным HTML
    web_view = ft.WebView(url=html_data_url, on_message=on_message)

    # Виджет для отображения снимка
    img = ft.Image()

    # Добавляем WebView и изображение на страницу
    page.add(web_view, img)

ft.app(target=main, view=ft.WEB_BROWSER)