import re
from datetime import datetime


class Field:
    """
    Базовий клас для всіх полів контакту.

    Зберігає значення та реалізує текстове представлення.
    """
    def __init__(self, value):
        """
        Ініціалізація поля.

        Args:
            value: Значення поля.
        """
        self.value = value

    def __str__(self):
        """
        Повертає текстове представлення значення.

        Returns:
            str: Значення як рядок.
        """
        return str(self.value)


class Name(Field):
    """
    Клас для збереження імені контакту.
    """
    pass


class Phone(Field):
    """
    Клас для збереження телефонного номера.

    Валідує, що номер складається рівно з 10 цифр.

    Raises:
        ValueError: якщо номер не містить рівно 10 цифр.
    """
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)


class Birthday(Field):
    """
    Клас для збереження дати народження.

    Зберігає значення як datetime-об'єкт.
    Формат дати: DD.MM.YYYY

    Raises:
        ValueError: якщо формат дати неправильний.
    """
    def __init__(self, value):
        try:
            date = datetime.strptime(value, "%d.%m.%Y")
            self.value = date
        except ValueError as exc:
            raise ValueError("Invalid date format. Use DD.MM.YYYY") from exc
        super().__init__(self.value)

    def __str__(self):
        """
        Повертає дату у форматі DD.MM.YYYY.

        Returns:
            str: Дата як рядок.
        """
        return self.value.strftime("%d.%m.%Y")

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

class Email(Field):
    """
    Клас для збереження email-адреси.

    Перевіряє, що значення відповідає базовому формату email.

    Raises:
        ValueError: якщо email має неправильний формат.
    """
    def __init__(self, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email format.")
        super().__init__(value)


class Address(Field):
    """
    Клас для збереження адреси.

    Перевіряє, що адреса не є порожньою.

    Raises:
        ValueError: якщо адреса порожня або складається лише з пробілів.
    """
    def __init__(self, value):
        if not value.strip():
            raise ValueError("Address cannot be empty.")
        super().__init__(value)
