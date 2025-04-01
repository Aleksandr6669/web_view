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

def get_translations(lang):
    # Получаем словарь для выбранного языка или для английского, если такого нет
    selected_lang = translations.get(lang, translations["en"])
    
    # Создаем словарь с переводами, если перевода для ключа нет, используем сам ключ
    return {key: selected_lang.get(key, key) for key in translations["en"]}
