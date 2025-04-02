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
    access_token = None  # Храним токен после авторизации

    languages = {
        "en": ("English", "🇬🇧"),
        "ua": ("Українська", "🇺🇦"),
        # "ru": ("Русский", "🇷🇺"),
    }

    def update_language(e):
        global tr
        current_lang = lang_dropdown.value
        tr = Translator(current_lang)
        update_ui()

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
        nonlocal access_token
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
            show_profile()
        else:
            show_message(response.json().get("message", "Error"))

    def show_profile():
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{API_URL}/profile", headers=headers)

        if response.status_code == 200:
            show_message(response.json().get("message", "Welcome!"), ft.colors.GREEN)
        else:
            show_message("Error loading profile", ft.colors.RED)
        container.width = page.width * 3.2
        container.height = page.height * 3.2
        # Логотип (в качестве примера, можно заменить на любой логотип)
        logo = ft.Image(src="https://via.placeholder.com/150", width=50, height=50)
        # Панель навигации с кнопками
        sidebar = ft.Container(
            bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLUE_GREY_900),
            blur=20,
            border_radius=20,
            width=page.width * 3.2,
            height=60,
            padding=ft.padding.only(left=20, right=20),
            content=ft.Row(
                [
                    # Логотип слева
                    logo,
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.ElevatedButton(text="Home", width=100),
                                ft.ElevatedButton(text="Profile", width=100),
                                ft.ElevatedButton(text="Settings", width=100),
                                ft.ElevatedButton(
                                    text="Logout",
                                    on_click=lambda e: page.go("/"),
                                    bgcolor=ft.colors.RED_500,
                                    color=ft.colors.WHITE,
                                    height=50,
                                    width=100
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                            spacing=10,
                        ),
                        expand=True,  # Контейнер, занимающий оставшееся пространство
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,  # Логотип слева
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        data_1 = [
            ft.LineChartData(
                data_points=[
                    ft.LineChartDataPoint(1, 1),
                    ft.LineChartDataPoint(3, 1.5),
                    ft.LineChartDataPoint(5, 1.4),
                    ft.LineChartDataPoint(7, 3.4),
                    ft.LineChartDataPoint(10, 2),
                    ft.LineChartDataPoint(12, 2.2),
                    ft.LineChartDataPoint(13, 1.8),
                ],
                stroke_width=8,
                color=ft.Colors.LIGHT_GREEN,
                curved=True,
                stroke_cap_round=True,
            ),
            ft.LineChartData(
                data_points=[
                    ft.LineChartDataPoint(1, 1),
                    ft.LineChartDataPoint(3, 2.8),
                    ft.LineChartDataPoint(7, 1.2),
                    ft.LineChartDataPoint(10, 2.8),
                    ft.LineChartDataPoint(12, 2.6),
                    ft.LineChartDataPoint(13, 3.9),
                ],
                color=ft.Colors.PINK,
                below_line_bgcolor=ft.Colors.with_opacity(0, ft.Colors.PINK),
                stroke_width=8,
                curved=True,
                stroke_cap_round=True,
            ),
            ft.LineChartData(
                data_points=[
                    ft.LineChartDataPoint(1, 2.8),
                    ft.LineChartDataPoint(3, 1.9),
                    ft.LineChartDataPoint(6, 3),
                    ft.LineChartDataPoint(10, 1.3),
                    ft.LineChartDataPoint(13, 2.5),
                ],
                color=ft.Colors.CYAN,
                stroke_width=8,
                curved=True,
                stroke_cap_round=True,
            ),
        ]

        chart = ft.LineChart(
            data_series=data_1,
            border=ft.Border(
                bottom=ft.BorderSide(4, ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE))
            ),
            left_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=1,
                        label=ft.Text("1m", size=14, weight=ft.FontWeight.BOLD),
                    ),
                    ft.ChartAxisLabel(
                        value=2,
                        label=ft.Text("2m", size=14, weight=ft.FontWeight.BOLD),
                    ),
                    ft.ChartAxisLabel(
                        value=3,
                        label=ft.Text("3m", size=14, weight=ft.FontWeight.BOLD),
                    ),
                    ft.ChartAxisLabel(
                        value=4,
                        label=ft.Text("4m", size=14, weight=ft.FontWeight.BOLD),
                    ),
                    ft.ChartAxisLabel(
                        value=5,
                        label=ft.Text("5m", size=14, weight=ft.FontWeight.BOLD),
                    ),
                    ft.ChartAxisLabel(
                        value=6,
                        label=ft.Text("6m", size=14, weight=ft.FontWeight.BOLD),
                    ),
                ],
                labels_size=40,
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=2,
                        label=ft.Container(
                            ft.Text(
                                "SEP",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE),
                            ),
                            margin=ft.margin.only(top=10),
                        ),
                    ),
                    ft.ChartAxisLabel(
                        value=7,
                        label=ft.Container(
                            ft.Text(
                                "OCT",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE),
                            ),
                            margin=ft.margin.only(top=10),
                        ),
                    ),
                    ft.ChartAxisLabel(
                        value=12,
                        label=ft.Container(
                            ft.Text(
                                "DEC",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE),
                            ),
                            margin=ft.margin.only(top=10),
                        ),
                    ),
                ],
                labels_size=32,
            ),
            tooltip_bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLUE_GREY),
            min_y=0,
            max_y=4,
            min_x=0,
            max_x=14,
            expand=True,
        )
        chart_cont = ft.Container(
            bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.BLUE_GREY_900,),
            blur = 20,
            border_radius=20,
            width=page.height*3.2,
            height=200,
            padding=20,
            content=chart
        )
        profile_content = ft.Column(
            [   
                sidebar,
                ft.Text(tr("welcome"), size=24, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                chart_cont,
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        # Обновляем контейнер с профилем
        container.content = profile_content
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
    
    # Динамическое обновление высоты
    def on_resize(e):
        page_height = page.height  # Обновляем высоту страницы

        # Обновляем расположение элементов в зависимости от доступного пространства
        # Например, сдвигаем элементы на страницу в зависимости от высоты
        container.height = page_height - 100  # Делаем пространство гибким для ввода

        page.update()


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
        bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_GREY_900,),
        blur = 20,
        width=350,
        height=415,
        border_radius=20,
        padding=20,
        animate=ft.Animation(duration=2050, curve="decelerate"),
        content=ft.Column([
            title,
            username,
            password,
            msg,
            login_btn,
            register_btn,
            lang_dropdown,
            
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
    update_ui()
    page.on_resize = on_resize

ft.app(target=main)
