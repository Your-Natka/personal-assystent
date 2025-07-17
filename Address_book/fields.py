import re
from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    """
    Клас для збереження телефонного номера з гнучкою валідацією.
    Дозволяє 10–15 цифр, з або без знаку '+'.
    """
    def __init__(self, value):
        # Забираємо все, крім цифр
        digits = ''.join(filter(str.isdigit, value))
        if not 10 <= len(digits) <= 15:
            raise ValueError("Phone number must contain 10–15 digits (excluding symbols).")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            date = datetime.strptime(value, "%d.%m.%Y")
            self.value = date
        except ValueError as exc:
            raise ValueError("Invalid date format. Use DD.MM.YYYY") from exc
        super().__init__(self.value)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

class Email(Field):
    def __init__(self, value):
        if not re.fullmatch(EMAIL_REGEX, value):
            raise ValueError("Invalid email format.")
        super().__init__(value)

class Address(Field):
    def __init__(self, value):
        if not value.strip():
            raise ValueError("Address cannot be empty.")
        super().__init__(value)