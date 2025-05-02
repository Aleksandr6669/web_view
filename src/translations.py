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
            "menu_title": "📂 Меню",
            "home": "Главная",
            "users": "Пользователи",
            "stats": "Статистика",
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
            "menu_title": "📂 Menu",
            "home": "Home",
            "users": "Users",
            "stats": "Statistics",
            "profile": "Profile",
            "settings": "Settings",
            "logout": "Logout",
            "refresh": "Refresh",
            "refresh_tooltip": "Restart interface if it glitches 🛠️"
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
            "menu_title": "📂 Меню",
            "home": "Головна",
            "users": "Користувачі",
            "stats": "Статистика",
            "profile": "Профіль",
            "settings": "Налаштування",
            "logout": "Вихід",
            "refresh": "Оновити",
            "refresh_tooltip": "Перезапустити інтерфейс, якщо щось зависло 🛠️"
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
            "menu_title": "📂 Menu",
            "home": "Accueil",
            "users": "Utilisateurs",
            "stats": "Statistiques",
            "profile": "Profil",
            "settings": "Paramètres",
            "logout": "Déconnexion",
            "refresh": "Rafraîchir",
            "refresh_tooltip": "Redémarrer l’interface en cas de bug 🛠️"
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
            "menu_title": "📂 菜单",
            "home": "主页",
            "users": "用户",
            "stats": "统计",
            "profile": "个人资料",
            "settings": "设置",
            "logout": "退出",
            "refresh": "刷新",
            "refresh_tooltip": "界面卡住时重新加载 🛠️"
        }
    }



    def __init__(self, page):
        # Инициализация с выбранным языком, по умолчанию используется английский
        self.page = page

    def __call__(self, key):
        lang = self.page.client_storage.get("current_lang") or "en"
        return self.translations.get(lang, {}).get(
            key, self.translations.get("en", {}).get(key, key)
        )


