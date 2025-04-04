class Translator:
    translations = {
        "ru": {
            "welcome": "Добро пожаловать в Поток!",
            "username": "Логин (Email)",
            "password": "Пароль",
            "login": "Войти",
            "register": "Регистрация",
            "user_exists": "Пользователь уже существует!",
            "reg_success": "Регистрация успешна!",
            "wrong_creds": "Неверные учетные данные!",
            "invalid_email": "Неверный адрес электронной почты!",
            "invalid_password": "Пароль должен содержать буквы и цифры и быть не менее 6 символов!",
            "remember_me": "Запомнить меня",
            "menu": "Меню",
            "profile": "Профиль",
            "settings": "Настройки",
            "logout": "Выход"
        },
        "en": {
            "welcome": "Welcome to Stream!",
            "username": "Username (Email)",
            "password": "Password",
            "login": "Login",
            "register": "Register",
            "user_exists": "User already exists!",
            "reg_success": "Registration successful!",
            "wrong_creds": "Incorrect credentials!",
            "invalid_email": "Invalid email address!",
            "invalid_password": "Password must contain letters and numbers and be at least 6 characters long!",
            "remember_me": "Remember me",
            "menu": "Menu",
            "profile": "Profile",
            "settings": "Settings",
            "logout": "Logout"
        },
        "ua": {
            "welcome": "Ласкаво просимо в Потік!",
            "username": "Логін (Email)",
            "password": "Пароль",
            "login": "Увійти",
            "register": "Реєстрація",
            "user_exists": "Користувач вже існує!",
            "reg_success": "Реєстрація успішна!",
            "wrong_creds": "Невірні облікові дані!",
            "invalid_email": "Невірна адреса електронної пошти!",
            "invalid_password": "Пароль повинен містити літери та цифри, і бути не менше 6 символів!",
            "remember_me": "Запам'ятати мене",
            "menu": "Меню",
            "profile": "Профіль",
            "settings": "Налаштування",
            "logout": "Вихід"
        },
        "fr": {
            "welcome": "Bienvenue dans Flux!",
            "username": "Nom d'utilisateur (Email)",
            "password": "Mot de passe",
            "login": "Connexion",
            "register": "S'inscrire",
            "user_exists": "L'utilisateur existe déjà !",
            "reg_success": "Inscription réussie !",
            "wrong_creds": "Identifiants incorrects !",
            "invalid_email": "Adresse e-mail invalide !",
            "invalid_password": "Le mot de passe doit contenir des lettres et des chiffres et comporter au moins 6 caractères !",
            "remember_me": "Se souvenir de moi",
            "menu": "Menu",
            "profile": "Profil",
            "settings": "Paramètres",
            "logout": "Déconnexion"
        },
        "zh": {
            "welcome": "欢迎来到流!",
            "username": "用户名 (Email)",
            "password": "密码",
            "login": "登录",
            "register": "注册",
            "user_exists": "用户已存在！",
            "reg_success": "注册成功！",
            "wrong_creds": "凭据错误！",
            "invalid_email": "无效的电子邮件地址！",
            "invalid_password": "密码必须包含字母和数字，并且至少6个字符！",
            "remember_me": "记住我",
            "menu": "菜单",
            "profile": "个人资料",
            "settings": "设置",
            "logout": "退出"
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

