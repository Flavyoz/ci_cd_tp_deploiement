# password_validator.py

def validate_password(password: str) -> dict:
    """
    Valide un mot de passe selon plusieurs règles de base.
    Retourne un dict avec le résultat global et le détail par règle.
    """
    errors = []

    if len(password) < 8:
        errors.append("Le mot de passe doit contenir au moins 8 caractères.")

    if not any(char.isupper() for char in password):
        errors.append("Le mot de passe doit contenir au moins une majuscule.")

    if not any(char.islower() for char in password):
        errors.append("Le mot de passe doit contenir au moins une minuscule.")

    if not any(char.isdigit() for char in password):
        errors.append("Le mot de passe doit contenir au moins un chiffre.")

    special_characters = "!@#$%^&*()-_=+[]{}|;:,.<>?/"
    if not any(char in special_characters for char in password):
        errors.append("Le mot de passe doit contenir au moins un caractère spécial.")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }