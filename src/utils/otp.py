import secrets


def generate_otp():
    return f"{secrets.randbelow(900000) + 100000}"
