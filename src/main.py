import flet as ft

def main(page: ft.Page):
    page.title = "Камера PWA"
    
    html_code = """
    <video id="camera" autoplay style="width: 100%;"></video>
    <script>
      const video = document.getElementById("camera");
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => video.srcObject = stream)
        .catch(err => console.error("Ошибка камеры:", err));
    </script>
    """
    
    page.add(ft.WebView(src_doc=html_code))

ft.app(target=main)