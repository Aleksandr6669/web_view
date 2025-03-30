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
    <h2>Видео с камеры</h2>
    <video id="video" width="640" height="480" autoplay></video>
    <script>
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function(stream) {
                document.getElementById('video').srcObject = stream;
            })
            .catch(function(error) {
                alert("Ошибка доступа к камере: " + error);
            });
    </script>
</body>
</html>
"""

def main(page: ft.Page):
    page.title = "Камера на Flet"

    # Кодируем HTML в data URL
    html_data_url = f"data:text/html;charset=utf-8,{camera_html}"

    # Создаем WebView с встроенным HTML
    web_view = ft.WebView(url=html_data_url)

    page.add(web_view)

ft.app(target=main, view=ft.WEB_BROWSER)