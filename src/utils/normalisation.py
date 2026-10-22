def normalise_name(name: str) -> str:
    return " ".join(name.split())

def normalise_email(email: str) -> str:
    return "".join(email.split()).lower()
