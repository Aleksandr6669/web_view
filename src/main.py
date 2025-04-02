import flet as ft
import re
import requests
from translations import Translator

API_URL = "https://alexsandr7779.pythonanywhere.com"  # Укажи здесь свой API, если он на другом сервере

tr = Translator()

def main(page: ft.Page):
    page.title = "Авторизация"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    # page.theme_mode = ft.ThemeMode.SYSTEM
    page.bgcolor = ft.colors.TRANSPARENT
    page.padding = 0

    current_lang = "en"

    languages = {
        "en": ("English", "🇬🇧"),
        "ua": ("Українська", "🇺🇦"),
        # "ru": ("Русский", "🇷🇺"),
    }


    def start_login():
        if page.client_storage.get("access_token") is not None:
            page.on_login()  # Вызываем событие на успешный вход
        else:
            page.on_logout(None)
            # page.on_logout()  # Вызываем событие на выход
    
    


    def update_language(e):
        global tr
        current_lang = lang.value
        page.client_storage.set("current_lang", current_lang)
        tr = Translator(current_lang)
        update_ui()

    def start_language():
        global tr
        if page.client_storage.get("current_lang") is not None:
            current_lang = page.client_storage.get("current_lang")
            
        tr = Translator(current_lang)

    def update_ui():
        title.value = tr("welcome")
        username.label = tr("username")
        password.label = tr("password")
        login_btn.text = tr("login")
        register_btn.text = tr("register")
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
        email = username.value
        password_value = password.value

        if not is_valid_email(email):
            show_message(tr("invalid_email"))
            return
        if not is_valid_password(password_value):
            show_message(tr("invalid_password"))
            return

        response = requests.post(f"{API_URL}/register", data={"username": email, "password": password_value})

        if response.status_code == 201:
            show_message(tr("reg_success"), ft.colors.GREEN)
        else:
            show_message(response.json().get("message", "Error"))

    def handle_login(e):
        email = username.value
        password_value = password.value

        if not is_valid_email(email):
            show_message(tr("invalid_email"))
            return
        if not is_valid_password(password_value):
            show_message(tr("invalid_password"))
            return

        response = requests.post(f"{API_URL}/login", data={"username": email, "password": password_value})

        if response.status_code == 200:
            access_token = response.json().get("access_token")
            show_message(tr("welcome") + f", {email}!", ft.colors.GREEN)
            page.client_storage.set("access_token", access_token)
            # show_profile()
            page.on_login()  # Вызываем событие на успешный вход
        else:
            show_message(response.json().get("message", "Error"))

    def show_profile():

        access_token = page.client_storage.get("access_token")
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{API_URL}/profile", headers=headers)

        if response.status_code == 200:
            # Логотип (в качестве примера, можно заменить на любой логотип)
            logo = ft.Image(src="https://via.placeholder.com/150", width=50, height=50)
            def handle_color_click(e):
                color = e.control.content.value
                print(f"{color}.on_click")
                page.update()

            def handle_on_hover(e):
                print(f"{e.control.content.value}.on_hover")

            # Кнопки с подменю
            menubar = ft.MenuBar(
                    style=ft.MenuStyle(
                        alignment=ft.alignment.top_right,
                        bgcolor=ft.Colors.BLUE_GREY_900,
                        mouse_cursor={
                            ft.ControlState.HOVERED: ft.MouseCursor.WAIT,
                            ft.ControlState.DEFAULT: ft.MouseCursor.ZOOM_OUT,
                        }),
                    controls=[
                        ft.SubmenuButton(
                            content=ft.Text(tr("BgColors")),
                            controls=[
                                ft.MenuItemButton(
                                    content=ft.Text("Blue"),
                                    leading=ft.Icon(ft.Icons.COLORIZE),
                                    style=ft.ButtonStyle(bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE}),
                                    on_click=handle_color_click,
                                    on_hover=handle_on_hover,
                                ),
                                ft.MenuItemButton(
                                    content=ft.Text("Green"),
                                    leading=ft.Icon(ft.Icons.COLORIZE),
                                    style=ft.ButtonStyle(bgcolor={ft.ControlState.HOVERED: ft.Colors.GREEN}),
                                    on_click=handle_color_click,
                                    on_hover=handle_on_hover,
                                ),
                                ft.MenuItemButton(
                                    content=ft.Text("Red"),
                                    leading=ft.Icon(ft.Icons.COLORIZE),
                                    style=ft.ButtonStyle(bgcolor={ft.ControlState.HOVERED: ft.Colors.RED}),
                                    on_click=handle_color_click,
                                    on_hover=handle_on_hover,
                                )
                            ]
                        ),
                    ]
                )

            # Кнопка для возврата на экран входа
            back_button = ft.ElevatedButton(
                text="Exit",
                on_click=close_app,
                bgcolor=ft.Colors.RED,
                color=ft.Colors.WHITE,
                height=50,
                width=200
            )

            # Панель навигации
            navbar = ft.Container(
                bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.BLUE_GREY_900),
                blur=20,
                border_radius=20,
                width=page.height * 3.2,
                content=ft.Row(
                    controls=[
                        logo,
                        ft.Container(
                            content=ft.Row(controls=[
                                menubar,
                                back_button,
                                ft.Container(
                                    width=20,
                                    height=20,
                                )
                            ]
                            )

                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    spacing=20
                )
            )

            
            # Основной контент профиля
            profile_content = ft.Column(
                [
                    navbar,
                    ft.Text("Welcome!", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )

            # Обновляем контейнер с профилем
            container.width = 2400
            container.height = 1800
            container.content = profile_content

        else:

            page.on_logout(None)

        page.update()
        
        

    title = ft.Text(tr("welcome"), size=24, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)

    def validate_email(value):
        if not value:  # Если поле пустое
            show_message("")
        elif not is_valid_email(value):  # Если email некорректный
            show_message(tr("invalid_email"), ft.colors.RED)
        else:
            show_message("")

    def validate_password(value):
        if not value:  # Если поле пустое
            show_message("")
        elif not is_valid_password(value):
            show_message(tr("invalid_password"), ft.colors.RED)
        else:
            show_message("")

    def close_app(e):
        page.on_logout(None) # Вызываем событие на выход
        page.session.clear()  # Очищаем данные сессии
    

    title = ft.Text(tr("welcome"), size=24, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)

    username = ft.TextField(
        label=tr("username"),
        width=300,
        border_radius=20,
        bgcolor=ft.colors.WHITE10,
        border_color=ft.colors.BLUE_500,
        focused_border_color=ft.colors.CYAN_400,
        text_style=ft.TextStyle(color=ft.colors.WHITE, size=14),
        on_change=lambda e: validate_email(username.value)
    )

    password = ft.TextField(
        label=tr("password"),
        password=True,
        width=300,
        border_radius=20,
        bgcolor=ft.colors.WHITE10,
        border_color=ft.colors.BLUE_500,
        focused_border_color=ft.colors.CYAN_400,
        text_style=ft.TextStyle(color=ft.colors.WHITE, size=14),
        on_change=lambda e: validate_password(password.value)
    )

    msg = ft.Text(color=ft.colors.WHITE)

    login_btn = ft.ElevatedButton(
        text=tr("login"),
        on_click=handle_login,
        bgcolor=ft.colors.BLUE_500,
        color=ft.colors.WHITE,
        height=50,
        width=200
    )

    register_btn = ft.ElevatedButton(
        text=tr("register"),
        on_click=handle_register,
        bgcolor=ft.colors.GREEN_500,
        color=ft.colors.WHITE,
        height=50,
        width=200
    )
    def lang_dropdown(page):
        if page.client_storage.get("current_lang") is not None:
            current_lang = page.client_storage.get("current_lang")

        return ft.Dropdown(
            
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
            content_padding=10,
        )

    lang = lang_dropdown(page)

    container = ft.Container(
        bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_GREY_900),
        blur = 20,
        width=350,
        height=415,
        # border_radius=20,
        padding=20,
        animate=ft.Animation(duration=850, curve="decelerate"),
        content=ft.Column([
            title,
            username,
            password,
            msg,
            login_btn,
            register_btn,
            lang,
            
        ],
        
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        animate_opacity=ft.animation.Animation(5000, ft.AnimationCurve.EASE_IN_OUT),  # Анимация прозрачности контента
        
        ),
        
    )
    


    def show_login_screen(e):
        
        profile_content = ft.Column(
            [
                title,
                username,
                password,
                msg,
                login_btn,
                register_btn,
                lang,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        # Обновляем контейнер с профилем
        container.width = 350
        container.height = 415
        container.content = profile_content
        

        page.update()

    background = ft.Image(
            src="/image/background.jpg",  # Путь к изображению

            width=page.width*3.2,
            height=page.height*3.2,      # Устанавливаем, как изображение должно быть вписано в контейнер
            fit=ft.ImageFit.COVER,        # Устанавливаем, чтобы изображение покрывало весь контейнер
            expand=True                   # Фон растягивается по размеру контейнера
        )

    body = ft.Stack(
            [   
                background,              # Добавляем фон первым
                container                 # Контейнер с остальными элементами
            ],
            width=page.width*3.2,
            height=page.height*3.2,
            alignment=ft.alignment.center,
            expand=True,                   # Растягиваем Stack на весь доступный размер
            
        )
    

    page.add(body)
    update_ui()
    # show_profile()
    page.on_logout = show_login_screen
    page.on_login = show_profile
    start_login()
    start_language()
    
   
ft.app(target=main)
# ft.app(target=main, port=8080, view=ft.WEB_BROWSER, assets_dir="assets")
