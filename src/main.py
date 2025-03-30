import flet as ft
import flet_webview as fwv

def main(page: ft.Page):
    # HTML-код для работы камеры
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Camera Access</title>
        <style>
            video {
                width: 100%;
                height: auto;
            }
        </style>
    </head>
    <body>
        <h1>Camera Stream</h1>
        <video id="camera" autoplay></video>
        <script>
            const video = document.getElementById("camera");
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(stream => video.srcObject = stream)
                .catch(err => console.error("Camera error:", err));
        </script>
    </body>
    </html>
    """

    # WebView для встроенного HTML
    wv = fwv.WebView(
        src_doc=html_code,
        on_page_started=lambda _: print("Page started"),
        on_page_ended=lambda _: print("Page ended"),
        on_web_resource_error=lambda e: print("Page error:", e.data),
        expand=True,
    )
    page.add(wv)

ft.app(main)