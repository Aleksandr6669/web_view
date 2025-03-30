import flet as ft
from flet_camera import Camera

def main(page: ft.Page):
    cam = Camera()
    page.add(cam)

ft.app(target=main)