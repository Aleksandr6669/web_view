class Translator:
    translations = {
        "ru": {
            "welcome": "Добро пожаловать!",
            "username": "Логин",
            "password": "Пароль",
            "login": "Войти",
            "register": "Регистрация",
            "user_exists": "Пользователь уже существует!",
            "reg_success": "Регистрация успешна!",
            "wrong_creds": "Неверные учетные данные!",
            "invalid_email": "Неверный адрес электронной почты!",
            "invalid_password": "Пароль должен содержать буквы и цифры и быть не менее 6 символов!"
        },
        "en": {
            "welcome": "Welcome!",
            "username": "Username",
            "password": "Password",
            "login": "Login",
            "register": "Register",
            "user_exists": "User already exists!",
            "reg_success": "Registration successful!",
            "wrong_creds": "Incorrect credentials!",
            "invalid_email": "Invalid email address!",
            "invalid_password": "Password must contain letters and numbers and be at least 6 characters long!"
        },
        "ua": {
            "welcome": "Ласкаво просимо!",
            "username": "Логін",
            "password": "Пароль",
            "login": "Увійти",
            "register": "Реєстрація",
            "user_exists": "Користувач вже існує!",
            "reg_success": "Реєстрація успішна!",
            "wrong_creds": "Невірні облікові дані!",
            "invalid_email": "Невірна адреса електронної пошти!",
            "invalid_password": "Пароль повинен містити літери та цифри, і бути не менше 6 символів!"
        }
    }

    def __init__(self, lang="en"):
        # Инициализация с выбранным языком, по умолчанию используется английский
        self.lang = lang

    def set_language(self, lang):
        # Изменяем язык
        if lang in self.translations:
            self.lang = lang
        else:
            print(f"Language '{lang}' not found, defaulting to 'en'.")
            self.lang = "en"

    def __call__(self, key):
        # Возвращаем перевод для заданного ключа, если такой ключ существует
        translations = self.translations.get(self.lang, self.translations["en"])
        return translations.get(key, f"Translation for '{key}' not found.")

