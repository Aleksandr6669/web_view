import flet as ft
import re
import requests
from translations import Translator

API_URL = "https://alexsandr7779.pythonanywhere.com"  # Укажи здесь свой API, если он на другом сервере


current_lang = "en"
tr = Translator(current_lang)

def main(page: ft.Page):
    page.title = tr("welcome")
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    # page.bgcolor = ft.Colors.TRANSPARENT
    page.padding = 0
    password_visible = ft.Ref[bool]()
    password_field = ft.Ref[ft.TextField]()

    

    languages = {
        "en": ("English  ", "🇬🇧 "),
        "ua": ("Українська  ", "🇺🇦 "),
        "fr": ("Français  ", "🇫🇷 "),
        "zh": ("中文  ", "🇨🇳 "),
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

        lang_popup(page)
        update_ui()
    
    

    def update_ui():
        title.value = tr("welcome")
        username.label = tr("username")
        password.label = tr("password")
        login_btn.text = tr("login")
        register_btn.text = tr("register")
        register_btn.text = tr("register")
        remember_me.label = tr("remember_me")
        # # Обновляем элементы в menubar
        # menubar.controls[0].content = ft.Text(tr("menu"))  # Название для SubmenuButton
        # menubar.controls[0].controls[0].content = ft.Text(tr("profile"))  # Профиль
        # menubar.controls[0].controls[1].content = ft.Text(tr("settings"))  # Настройки
        # menubar.controls[0].controls[2].content = ft.Text(tr("logout"))  # Выход

        menubar.items[0].text = tr("profile")    # Профиль
        menubar.items[1].text = tr("settings")   # Настройки
        menubar.items[3].text = tr("logout")     # Выход

        navigation_panel.content.controls[0].value = tr("menu_title")


        nav_refs["home"].current.content.controls[1].value = tr("home")
        nav_refs["users"].current.content.controls[1].value = tr("users")
        nav_refs["stats"].current.content.controls[1].value = tr("stats")
        nav_refs["settings"].current.content.controls[1].value = tr("settings")

        refresh_button.text = tr("refresh")
        refresh_button.tooltip = tr("refresh_tooltip")

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
        global is_login_screen
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
            is_login_screen = False
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
                    main_area
                    
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

    def lang_popup(page):
        try:
            current_lang = page.client_storage.get("current_lang") or "en"
        except:
            current_lang = "en"

         # Теперь на основе current_lang создаём красивую надпись
        selected_text = ft.Text(f"{languages.get(current_lang)[1]} {languages.get(current_lang)[0]}", size=14, weight=ft.FontWeight.W_600)

        def handle_lang_select(e):
            selected_lang = e.control.data
            page.client_storage.set("current_lang", selected_lang)
            global tr
            tr = Translator(selected_lang)
            
            # Обновляем надпись на кнопке
            selected_text.value = f"{languages[selected_lang][1]} {languages[selected_lang][0]}"
            
            update_ui()
            page.update()

        return ft.PopupMenuButton(
            tooltip="",
            content=selected_text,
            menu_position=ft.PopupMenuPosition.UNDER,
            bgcolor=ft.Colors.BLUE_GREY,
            items=[
                ft.PopupMenuItem(
                    text=f"{flag} {name}",
                    data=k,
                    on_click=handle_lang_select,
                )
                for k, (name, flag) in languages.items()
            ],
        )

            
    lang = lang_popup(page)
    
    title = ft.Text(tr("welcome"), size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)

    # Предположим, у вас уже есть логотип (например, изображение или текст)
    logo = ft.Image(src="icon.png", width=100, height=50)

    avatar_url = "avatar.png"
    menubar = ft.PopupMenuButton(
        tooltip="",
        # Содержимое кнопки — тот самый Stack, который ты отправил
        content=ft.Stack(
            [
                ft.CircleAvatar(foreground_image_src=avatar_url),
                ft.Container(
                    content=ft.CircleAvatar(bgcolor=ft.colors.GREEN, radius=5),
                    alignment=ft.alignment.bottom_left,
                ),
            ],
            width=40,
            height=40,
        ),

        # Меню появляется ПОД аватаркой
        menu_position=ft.PopupMenuPosition.UNDER,
        bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLUE_GREY_700),

        # Пункты меню
        items=[
            ft.PopupMenuItem(icon=ft.Icons.PERSON, text=tr("profile")),
            ft.PopupMenuItem(icon=ft.Icons.SETTINGS, text=tr("settings")),
            ft.PopupMenuItem(),  # Divider
            ft.PopupMenuItem(icon=ft.Icons.EXIT_TO_APP, text=tr("logout"), on_click=close_app),
        ],
    )

    refresh_button = ft.ElevatedButton(
        text=tr("refresh"),
        tooltip=tr("refresh_tooltip"),
        icon=ft.icons.REFRESH,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            bgcolor=ft.colors.BLUE_500,
            color=ft.colors.WHITE,
            overlay_color=ft.colors.BLUE_100,
            padding=ft.padding.symmetric(horizontal=20, vertical=12),
            elevation=3,
        ),
        on_click=lambda e: reset_ui()
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
                                refresh_button,
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


    users = [
        {"username": "alice", "email": "alice@example.com"},
        {"username": "bob", "email": "bob@example.com"},
        {"username": "charlie", "email": "charlie@example.com"},
        {"username": "alice", "email": "alice@example.com"},
        {"username": "bob", "email": "bob@example.com"},
        {"username": "charlie", "email": "charlie@example.com"},
        {"username": "alice", "email": "alice@example.com"},
        {"username": "bob", "email": "bob@example.com"},
        {"username": "charlie", "email": "charlie@example.com"},
    ]

    user_cards = [
        ft.Container(
            bgcolor=ft.Colors.BLUE_GREY_100,
            border_radius=12,
            padding=15,
            margin=10,
            animate_opacity=300,
            opacity=1.0,
            content=ft.Row([
                ft.CircleAvatar(foreground_image_src=avatar_url),
                ft.Text(f"👤 {user['username']}", size=16, weight=ft.FontWeight.BOLD),
                ft.Text(f"📧 {user['email']}", size=14, color=ft.Colors.BLUE_GREY_700),
            ])
        )
        for user in users
    ]

    active_view = ft.Ref[str]()     # создаём ссылку
    active_view.current = "home"    # и только потом кладём значение


    home_view = ft.Container(
        expand=True,
        padding=15,
        border_radius=10,
        height=page.height - 150,
        width=page.width*3.2,
        bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_GREY_500),
        content=ft.Text("🏠 Добро пожаловать на главную!", size=24),
        visible=True,
        opacity=1.0,
        animate_opacity=200
    )

    users_view = ft.Container(
        expand=True,
        padding=15,
        border_radius=10,
        height=page.height - 150,
        width=page.width*3.2,
        bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_GREY_500),
        content=ft.Column(
            controls=[
                ft.Text("Зарегистрированные пользователи:", size=20, color=ft.Colors.WHITE),

                ft.Container(
                    expand=True,
                    content=ft.Column(
                        expand=True,
                        scroll=ft.ScrollMode.AUTO,
                        spacing=10,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=user_cards,
                    )
                )
            ],
            spacing=15,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        visible=False,
        opacity=0.0,
        animate_opacity=200
    )


    stats_view = ft.Container(
        expand=True,
        padding=15,
        border_radius=10,
        height=page.height - 150,
        width=page.width*3.2,
        bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_GREY_500),
        content=ft.Text("📊 Аналитика и статистика", size=24),
        visible=False,
        opacity=0.0,
        animate_opacity=200
    )

    settings_view = ft.Container(
        expand=True,
        padding=15,
        border_radius=10,
        height=page.height - 150,
        width=page.width*3.2,
        bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_GREY_500),
        content=ft.Text("⚙️ Настройки приложения", size=24),
        visible=False,
        opacity=0.0,
        animate_opacity=200
    )

    views = {
        "home": home_view,
        "users": users_view,
        "stats": stats_view,
        "settings": settings_view
    }

    nav_refs = {
        "home": ft.Ref[ft.Container](),
        "users": ft.Ref[ft.Container](),
        "stats": ft.Ref[ft.Container](),
        "settings": ft.Ref[ft.Container]()
    }

    def switch_view(view_key):
        active_view.current = view_key
        for key, view in views.items():
            if key == view_key:
                view.visible = True
                view.opacity = 1.0
            else:
                view.opacity = 0.0
            view.update()

        for key, ref in nav_refs.items():
            if ref.current:
                ref.current.bgcolor = ft.Colors.BLUE_GREY_100 if key == view_key else None
                ref.current.update()

    def nav_item(key, icon, label):
        return ft.Container(
            ref=nav_refs[key],
            padding=ft.padding.symmetric(vertical=10, horizontal=10),
            border_radius=8,
            bgcolor=ft.Colors.BLUE_GREY_100 if key == "home" else None,
            content=ft.Row(
                controls=[
                    ft.Icon(icon, size=20, color=ft.Colors.BLUE_GREY_700),
                    ft.Text(label, color=ft.Colors.BLUE_GREY_800, size=14)
                ],
                spacing=10
            ),
            on_click=lambda e: switch_view(key),
            ink=True
        )
    
    navigation_panel = ft.Container(
        width=200,
        padding=15,
        bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_GREY_500),
        border_radius=15,
        content = ft.Column(
            controls=[
                ft.Text(tr("menu_title"), size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.LIGHT_BLUE_900),
                ft.Divider(thickness=1, color=ft.Colors.BLUE_GREY_100),
                nav_item("home", ft.icons.HOME_ROUNDED, tr("home")),
                nav_item("users", ft.icons.PEOPLE_ALT_OUTLINED, tr("users")),
                nav_item("stats", ft.icons.BAR_CHART, tr("stats")),
                nav_item("settings", ft.icons.SETTINGS, tr("settings")),
            ],
            spacing=8
        )

    )

    main_area = ft.Container(
        blur=20,
        # width=2400,
        
        padding=20,
        content=ft.Row(
            controls=[
                navigation_panel,
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        expand=True,
                        controls=[
                            ft.Stack(
                                expand=True,
                                controls=[
                                    home_view,
                                    users_view,
                                    stats_view,
                                    settings_view
                                ]
                            )
                        ]
                    )
                )
            ],
            spacing=30,
            vertical_alignment=ft.CrossAxisAlignment.START
        )
    )


            
    username = ft.TextField(
        label=tr("username"),
        width=300,
        height=50,
        border_radius=20,
        bgcolor=ft.Colors.WHITE10,
        border_color=ft.Colors.BLUE_500,
        focused_border_color=ft.Colors.CYAN_400,
        text_style=ft.TextStyle(color=ft.Colors.WHITE, size=16),
        on_change=lambda e: validate_email(username.value)
    )
    username.auto_focus = True

    def toggle_visibility(e):
        password_visible.current = not password_visible.current
        password_field.current.password = not password_visible.current
        password_field.current.suffix = ft.IconButton(
            icon=ft.icons.VISIBILITY_OFF if password_visible.current else ft.icons.VISIBILITY,
            on_click=toggle_visibility,
            icon_color=ft.Colors.BLUE_300,
        )
        password_field.current.update()

    password = ft.TextField(
        label=tr("password"),
        password=True,
        # suffix=ft.Container(
        #     content=ft.IconButton(
        #         icon=ft.icons.VISIBILITY,
        #         on_click=toggle_visibility,
        #         icon_color=ft.Colors.BLUE_300,
        #         icon_size=20,
        #         style=ft.ButtonStyle(padding=2),
        #     ),
        #     width=20,
        #     height=20,
        #     alignment=ft.alignment.center,
        # ),
        width=300,
        height=50,
        text_style=ft.TextStyle(color=ft.Colors.WHITE, size=14),
        text_vertical_align=ft.VerticalAlignment.CENTER,
        border_radius=20,
        bgcolor=ft.Colors.WHITE10,
        border_color=ft.Colors.BLUE_500,
        focused_border_color=ft.Colors.CYAN_400,
        on_change=lambda e: validate_password(password.value)
    )

    msg = ft.Text(color=ft.Colors.WHITE, height=50)

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
        global is_login_screen
        is_login_screen = True
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
        container.width = 355
        container.height = 470
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
    
    def reset_ui():
        page.clean()
        main(page)
        page.on_login()

        # container.content.controls.clear()
        # container.content.update()
        # show_profile()

    def handle_key(e: ft.KeyboardEvent):
        if e.key == "Enter" and is_login_screen:
            handle_login(e)



    page.add(body)
    
    page.on_keyboard_event = handle_key
    page.on_logout = show_login_screen
    page.on_login = show_profile
    
    start_login()
    
    
   
# ft.app(target=main)
ft.app(target=main, port=8080, view=ft.WEB_BROWSER, assets_dir="assets")
