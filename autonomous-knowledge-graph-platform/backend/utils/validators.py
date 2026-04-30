from config.security import ALLOWED_EXTENSIONS


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def password_strength_error(password):
    password = password or ""
    checks = [
        (len(password) >= 12, "at least 12 characters"),
        (any(char.islower() for char in password), "one lowercase letter"),
        (any(char.isupper() for char in password), "one uppercase letter"),
        (any(char.isdigit() for char in password), "one number"),
        (any(not char.isalnum() for char in password), "one special character"),
    ]
    missing = [message for passed, message in checks if not passed]
    if missing:
        return "Password must include " + ", ".join(missing) + "."
    return None
