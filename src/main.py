import flet as ft

def main(page: ft.Page):
    page.title = "Видеоискатель в браузере (Flet + JS)"

    # Встраиваем HTML + JavaScript прямо в WebView
    camera_html = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Видео с камеры</title>
    </head>
    <body>
        <h2>Видеоискатель</h2>
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

    # Кодируем HTML в data URL
    html_data_url = f"data:text/html;charset=utf-8,{camera_html}"

    # Создаём WebView с этим кодом
    web_view = ft.WebView(url=html_data_url)

    page.add(ft.Text("Видео с камеры"))
    page.add(web_view)

ft.app(target=main, view=ft.WEB_BROWSER)