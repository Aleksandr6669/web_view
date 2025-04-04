import flet as ft
import re
import requests
from translations import Translator

API_URL = "https://alexsandr7779.pythonanywhere.com"  # Укажи здесь свой API, если он на другом сервере


current_lang = "en"
tr = Translator(current_lang)

def main(page: ft.Page):
    page.title = "Авторизация"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    # page.theme_mode = ft.ThemeMode.LIGHT
    # page.bgcolor = ft.Colors.TRANSPARENT
    page.padding = 0

    

    languages = {
        "en": ("English", "🇬🇧"),
        "ua": ("Українська", "🇺🇦"),
        "fr": ("Français", "🇫🇷"),
        "zh": ("中文", "🇨🇳"),
        # "ru": ("Русский", "🇷🇺"),
    }



    def start_login():
        global tr
        try:
            if page.client_storage.get("access_token") is not None and page.client_storage.get("remember_me") == True:
                page.on_login()  # Вызываем событие на успешный вход
            else:
                page.on_logout(None)
                # page.on_logout()  # Вызываем событие на 
        except:
            page.on_logout(None)
        try:
            if page.client_storage.get("current_lang") is not None:
                current_lang = page.client_storage.get("current_lang")
            else:
                current_lang = "en"
                page.client_storage.set("current_lang", current_lang)
        except:
            current_lang = "en"

        tr = Translator(current_lang)

        update_ui()
    
    


    def update_language(e):
        global tr
        current_lang = lang.value
        page.client_storage.set("current_lang", current_lang)
        tr = Translator(current_lang)
        update_ui()


    def update_ui():
        title.value = tr("welcome")
        username.label = tr("username")
        password.label = tr("password")
        login_btn.text = tr("login")
        register_btn.text = tr("register")
        register_btn.text = tr("register")
        remember_me.label = tr("remember_me")
        # Обновляем элементы в menubar
        menubar.controls[0].content = ft.Text(tr("menu"))  # Название для SubmenuButton
        menubar.controls[0].controls[0].content = ft.Text(tr("profile"))  # Профиль
        menubar.controls[0].controls[1].content = ft.Text(tr("settings"))  # Настройки
        menubar.controls[0].controls[2].content = ft.Text(tr("logout"))  # Выход
        page.update()

    def show_message(text, color=ft.Colors.ERROR):
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
            show_message(tr("reg_success"), ft.Colors.LIGHT_GREEN_400)
        else:
            show_message(response.json().get("message", "Error"))

    def handle_login(e):
        email = username.value
        password_value = password.value
        page.client_storage.set("remember_me", remember_me.value)
        page.client_storage.set("saved_username", username.value)

        if not is_valid_email(email):
            show_message(tr("invalid_email"))
            return
        if not is_valid_password(password_value):
            show_message(tr("invalid_password"))
            return

        response = requests.post(f"{API_URL}/login", data={"username": email, "password": password_value})

        if response.status_code == 200:
            access_token = response.json().get("access_token")
            show_message(tr("welcome") + f", {email}!", ft.Colors.LIGHT_GREEN_400)
            page.client_storage.set("access_token", access_token)
            # show_profile()
            page.on_login()  # Вызываем событие на успешный вход
        else:
            show_message(response.json().get("message", "Error"))
        password.value = ""

    def show_profile():
        access_token = page.client_storage.get("access_token")
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{API_URL}/profile", headers=headers)


        if response.status_code == 200:
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
            container.padding=0
            container.width = 2400
            container.height = 1800
            container.content = profile_content

        else:

            page.on_logout(None)

        page.update()
        
    def validate_email(value):
        if not value:  # Если поле пустое
            show_message("")
        elif not is_valid_email(value):  # Если email некорректный
            show_message(tr("invalid_email"), ft.Colors.ERROR)
        else:
            show_message("")

    def validate_password(value):
        if not value:  # Если поле пустое
            show_message("")
        elif not is_valid_password(value):
            show_message(tr("invalid_password"), ft.Colors.ERROR)
        else:
            show_message("")

    def close_app(e):
        page.client_storage.remove("access_token")  # Удаляем токен доступа
        page.client_storage.remove("remember_me")
        page.on_logout(None) # Вызываем событие на выход
        page.session.clear()  # Очищаем данные сессии

    def handle_color_click(e):
        print(f".on_click")
        page.update()

    def handle_on_hover(e):
        print(f".on_hover")

    def lang_dropdown(page):
        try:
            if page.client_storage.get("current_lang") is not None:
                current_lang = page.client_storage.get("current_lang")
            else:
                current_lang = "en"
        except:
            current_lang = "en"

        return ft.Dropdown(
            
            value=current_lang,
            options=[
                ft.dropdown.Option(k, text=f"{flag} {name}")
                for k, (name, flag) in languages.items()
            ],
            selected_suffix=ft.Text(languages[current_lang][1]),  # Только флаг в поле выбора
            on_change=update_language,
            bgcolor=ft.Colors.BLUE_GREY_900,
            color=ft.Colors.WHITE,
            border_width=0,  # Убираем обводку
            border_radius=20,
            text_size=12,
            content_padding=0,
            width=140,

        )

    lang = lang_dropdown(page)
    
    title = ft.Text(tr("welcome"), size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)

    # Предположим, у вас уже есть логотип (например, изображение или текст)
    logo = ft.Image(src="icon.png", width=100, height=50)

    menubar = ft.MenuBar(
                controls=[
                    ft.SubmenuButton(
                        height=30,
                        animate_size=3000,
                        content=ft.Text(tr("menu")),
                        controls=[
                            ft.MenuItemButton(
                                content=ft.Text(tr("profile")),
                                leading=ft.Icon(ft.Icons.PERSON),
                                on_click=handle_color_click,
                                style=ft.ButtonStyle(
                                    text_style=ft.TextStyle(
                                        color=ft.Colors.WHITE,  # Цвет текста
                                        size=12,  # Размер текста
                                        weight=ft.FontWeight.NORMAL,  # Жирность текста
                                        font_family="Arial",  # Шрифт текста
                                    ),
                                    bgcolor=ft.Colors.BLACK54,  # Тусклый цвет текста
                                    elevation=0,  # Без тени
                                    shape=ft.RoundedRectangleBorder(radius=0),  # Закругленные углы
                                )
                            ),
                            ft.MenuItemButton(
                                content=ft.Text(tr("settings")),
                                leading=ft.Icon(ft.Icons.SETTINGS),
                                on_click=handle_color_click,

                                style=ft.ButtonStyle(
                                    text_style=ft.TextStyle(
                                        color=ft.Colors.WHITE,  # Цвет текста
                                        size=12,  # Размер текста
                                        weight=ft.FontWeight.NORMAL,  # Жирность текста
                                        font_family="Arial",  # Шрифт текста
                                    ),
                                    bgcolor=ft.Colors.BLACK54,
                                    elevation=0,
                                    shape=ft.RoundedRectangleBorder(radius=0),
                                )
                            ),
                            ft.MenuItemButton(
                                content=ft.Text(tr("logout")),
                                leading=ft.Icon(ft.Icons.EXIT_TO_APP),  # Иконка для выхода
                                style=ft.ButtonStyle(
                                    text_style=ft.TextStyle(
                                        color=ft.Colors.WHITE,  # Цвет текста
                                        size=12,  # Размер текста
                                        weight=ft.FontWeight.NORMAL,  # Жирность текста
                                        font_family="Arial",  # Шрифт текста
                                    ),
                                    bgcolor={ft.ControlState.HOVERED: ft.Colors.RED_600},
                                    elevation=0,
                                    shape=ft.RoundedRectangleBorder(radius=0),
                                ),
                                on_click=close_app,
                            )
                        ],
                        
                    ),
                ]
            )
    # Панель навигации
    navbar = ft.Container(
                bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_GREY_500),
                blur=20,
                # border_radius=20,
                width=2400,
                height=60,
                content=ft.Row(
                    controls=[
                        logo,
                        ft.Container(
                            alignment=ft.alignment.center,  # Центрируем содержимое контейнера
                            content=ft.Row(
                                height=40,
                                controls=[
                                lang,
                                menubar,
                                ft.Container(
                                    width=20,
                                    height=20,
                                )
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Центрируем элементы по вертикали
                            alignment=ft.MainAxisAlignment.CENTER,  # Центрируем элементы в строке
                            )

                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Центрируем элементы по вертикали
                    spacing=20
                )
            )

            
    username = ft.TextField(
        label=tr("username"),
        width=300,
        border_radius=20,
        bgcolor=ft.Colors.WHITE10,
        border_color=ft.Colors.BLUE_500,
        focused_border_color=ft.Colors.CYAN_400,
        text_style=ft.TextStyle(color=ft.Colors.WHITE, size=14),
        on_change=lambda e: validate_email(username.value)
    )
    username.auto_focus = True

    password = ft.TextField(
        label=tr("password"),
        password=True,
        width=300,
        border_radius=20,
        bgcolor=ft.Colors.WHITE10,
        border_color=ft.Colors.BLUE_500,
        focused_border_color=ft.Colors.CYAN_400,
        text_style=ft.TextStyle(color=ft.Colors.WHITE, size=14),
        on_change=lambda e: validate_password(password.value)
    )

    msg = ft.Text(color=ft.Colors.WHITE)

    login_btn = ft.ElevatedButton(
        text=tr("login"),
        on_click=handle_login,
        bgcolor=ft.Colors.BLUE_500,
        color=ft.Colors.WHITE,
        height=50,
        width=200
    )

    register_btn = ft.ElevatedButton(
        text=tr("register"),
        on_click=handle_register,
        bgcolor=ft.Colors.GREEN_500,
        color=ft.Colors.WHITE,
        height=50,
        width=200
    )
    remember_me = ft.Checkbox(label=tr("remember_me"), value=False)

    

    

    def show_login_screen(e):
        username.value = page.client_storage.get("saved_username")
        forma_content = ft.Column(
            [
                title,
                username,
                password,
                remember_me,
                msg,
                login_btn,
                register_btn,
                lang,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        # Обновляем контейнер с профилем
        container.padding=20
        container.width = 350
        container.height = 440
        container.content = forma_content
        

        page.update()



    container = ft.Container(
        bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_GREY_900),
        blur = 20,
        width=0,
        height=0,
        # padding=20,
        animate=ft.Animation(duration=350, curve="decelerate"),
        content=ft.Column([

        ],

        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),

    )

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
    
    # show_profile()
    page.on_logout = show_login_screen
    page.on_login = show_profile
    
    start_login()
    
    
   
# ft.app(target=main)
ft.app(target=main, port=8080, view=ft.WEB_BROWSER, assets_dir="assets")
