import flet as ft
import re
import requests
from translations import get_translations

API_URL = "https://alexsandr7779.pythonanywhere.com"  # Укажи здесь свой API, если он на другом сервере

def main(page: ft.Page):
    page.title = "Авторизация"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.SYSTEM

    # Градиентный фон
    page.bgcolor = ft.LinearGradient(
        begin=ft.alignment.top_center,
        end=ft.alignment.bottom_center,
        colors=[ft.colors.BLUE, ft.colors.YELLOW]
    )

    current_lang = "ru"
    access_token = None  # Храним токен после авторизации

    languages = {
        "ru": ("Русский", "🇷🇺"),
        "en": ("English", "🇬🇧"),
        "ua": ("Українська", "🇺🇦"),
    }

    def update_language(e):
        nonlocal current_lang
        current_lang = lang_dropdown.value
        update_ui()

    def update_ui():
        tr = get_translations(current_lang)
        title.value = tr["welcome"]
        username.label = tr["username"]
        password.label = tr["password"]
        login_btn.text = tr["login"]
        register_btn.text = tr["register"]
        page.update()

    def show_message(text, color=ft.colors.RED):
        msg.value = text
        msg.color = color
        page.update()

    def is_valid_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def is_valid_password(password):
        return len(password) >= 6 and re.search(r"[a-zA-Z]", password) and re.search(r"\d", password)

    def handle_register(e):
        tr = get_translations(current_lang)
        email = username.value
        password_value = password.value

        if not is_valid_email(email):
            show_message(tr.get("invalid_email", "invalid_email"))
            return
        if not is_valid_password(password_value):
            show_message(tr.get("invalid_password", "invalid_password"))
            return

        response = requests.post(f"{API_URL}/register", data={"username": email, "password": password_value})

        if response.status_code == 201:
            show_message(tr.get("reg_success", "reg_success"), ft.colors.GREEN)
        else:
            show_message(response.json().get("message", "Error"))

    def handle_login(e):
        nonlocal access_token
        tr = get_translations(current_lang)
        email = username.value
        password_value = password.value

        if not is_valid_email(email):
            show_message(tr.get("invalid_email", "invalid_email"))
            return
        if not is_valid_password(password_value):
            show_message(tr.get("invalid_password", "invalid_password"))
            return

        response = requests.post(f"{API_URL}/login", data={"username": email, "password": password_value})

        if response.status_code == 200:
            access_token = response.json().get("access_token")
            show_message(tr.get("welcome", "welcome") + f", {email}!", ft.colors.GREEN)
            load_profile()
        else:
            show_message(response.json().get("message", "Error"))

    def load_profile():
        nonlocal access_token
        if not access_token:
            return

        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{API_URL}/profile", headers=headers)

        if response.status_code == 200:
            show_message(response.json().get("message", "Welcome!"), ft.colors.GREEN)
        else:
            show_message("Ошибка при загрузке профиля")

    def validate_email(value):
        if not is_valid_email(value):
            show_message("Некорректный email")
        else:
            show_message("")

    def validate_password(value):
        if not is_valid_password(value):
            show_message("Пароль должен содержать минимум 6 символов, цифры и буквы")
        else:
            show_message("")

    tr = get_translations(current_lang)

    title = ft.Text(tr["welcome"], size=24, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)

    username = ft.TextField(
        label=tr["username"],
        width=200,
        border_radius=20,
        bgcolor=ft.colors.WHITE10,
        border_color=ft.colors.BLUE_500,
        focused_border_color=ft.colors.CYAN_400,
        text_style=ft.TextStyle(color=ft.colors.WHITE, size=14),
        on_change=lambda e: validate_email(username.value)
    )

    password = ft.TextField(
        label=tr["password"],
        password=True,
        width=200,
        border_radius=20,
        bgcolor=ft.colors.WHITE10,
        border_color=ft.colors.BLUE_500,
        focused_border_color=ft.colors.CYAN_400,
        text_style=ft.TextStyle(color=ft.colors.WHITE, size=14),
        on_change=lambda e: validate_password(password.value)
    )

    msg = ft.Text(color=ft.colors.WHITE)

    login_btn = ft.ElevatedButton(
        text=tr["login"],
        on_click=handle_login,
        bgcolor=ft.colors.BLUE_500,
        color=ft.colors.WHITE,
        height=50,
        width=200
    )

    register_btn = ft.ElevatedButton(
        text=tr["register"],
        on_click=handle_register,
        bgcolor=ft.colors.GREEN_500,
        color=ft.colors.WHITE,
        height=50,
        width=200
    )

    lang_dropdown = ft.Dropdown(
        value=current_lang,
        options=[
            ft.dropdown.Option(k, text=f"{flag} {name}")
            for k, (name, flag) in languages.items()
        ],
        on_change=update_language,
        bgcolor=ft.colors.BLUE_GREY_900,
        color=ft.colors.WHITE,
        focused_bgcolor=ft.colors.BLUE_700,
        border_width=0,  # Убираем обводку
        # border_color=None,  # Убираем обводку
        # focused_border_color=None,  # Убираем обводку при 
        border_radius=20,
        text_size=16,
        content_padding=10
    )

    container = ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.colors.BLUE, ft.colors.YELLOW]
        ),
        content=ft.Column([
            title,
            username,
            password,
            login_btn,
            register_btn,
            msg,
            lang_dropdown
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        width=1850,
    )

    page.add(container)
    update_ui()

ft.app(target=main)
