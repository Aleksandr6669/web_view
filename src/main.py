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
            // Отправка данных в Flet через window.postMessage
            window.parent.postMessage(imageData, "*");
        };
    </script>
</body>
</html>
"""

def main(page: ft.Page):
    page.title = "Камера на Flet"

    # Кодируем HTML в data URL
    html_data_url = f"data:text/html;charset=utf-8,{camera_html}"

    # Виджет для отображения снимка
    img = ft.Image()

    # Создаем WebView с встроенным HTML
    web_view = ft.WebView(url=html_data_url)

    # Функция для получения данных изображения
    def get_image_from_webview(e):
        page.add(img)  # Отобразим изображение на странице
        img.src_base64 = e.message  # Устанавливаем полученное изображение
        page.update()

    # Регистрируем обработчик сообщений из WebView
    web_view.on_message = get_image_from_webview

    # Добавляем WebView на страницу
    page.add(web_view)

ft.app(target=main, view=ft.WEB_BROWSER)