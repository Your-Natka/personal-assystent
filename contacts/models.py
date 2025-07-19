# Дані та логіка
from collections import UserDict
from datetime import datetime
import pickle
from colorama import Fore, Style
from pathlib import Path
import re

# Базовий клас для полів
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Клас для зберігання імені
class Name(Field):
    def __init__(self, value):
        if not value or not value.strip():  # Перевірка на порожнє або пробільне ім'я
            raise ValueError("Name cannot be empty.")
        super().__init__(value)

# Клас для зберігання телефону з валідацією формату
class Phone(Field):
    def __init__(self, value):
        # Валідація українського номеру: 10 цифр
        ukr_pattern = r"^\d{10}$"

        # Валідація міжнародного формату: +код країни та 11-15 цифр
        intl_pattern = r"^\+\d{11,15}$"

        # Перевірка, чи весь рядок повністю відповідає одному з шаблонів (український або міжнародний номер)
        if not re.fullmatch(ukr_pattern, value) and not re.fullmatch(intl_pattern, value):
            raise ValueError(
                "Phone number must be 10 digits (e.g., 0671234567) or international format starting with '+' (e.g., +4915112345678)."
            )
        super().__init__(value)

# Клас для зберігання дня народження з перевіркою формату DD.MM.YYYY
class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Birthday must be in DD.MM.YYYY format. For example: 01.01.2000")
        super().__init__(value)

# Клас для зберігання електронної пошти з валідацією
class Email(Field):
    def __init__(self, value):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not re.fullmatch(pattern, value):
            raise ValueError(
                "Invalid email address format. Please use a format like 'example@mail.com' or 'john.doe@example.co.uk'."
            )
        super().__init__(value)

# Клас для зберігання адреси (без спеціальної валідації)
class Address(Field):
    def __init__(self, value):
        if not value.strip():
            raise ValueError("Address cannot be empty.")
        super().__init__(value)


# Створення контактного запису
class Contact:
    def __init__(self, name, phones=None, birthday=None, email=None, address=None):
        self.name = Name(name)  # ✅ Валідація і обгортка
        self.phones = [Phone(p) for p in phones] if phones else []
        self.birthday = Birthday(birthday) if birthday else None
        self.email = Email(email) if email else None
        self.address = Address(address) if address else None

    # Метод __str__ використовується для перетворення об'єкта в рядок під час друку.
    def __str__(self):
        # телефони відображаються як перелік, або "N/A" якщо їх немає
        phones_str = ", ".join(str(p) for p in self.phones) if self.phones else "N/A"
        # день народження, email і адреса — аналогічно
        bday_str = str(self.birthday) if self.birthday else "N/A"
        email_str = str(self.email) if self.email else "N/A"
        address_str = str(self.address) if self.address else "N/A"
        return f"Name: {self.name}, Phones: {phones_str}, Birthday: {bday_str}, Email: {email_str}, Address: {address_str}"

# Книга контактів
class AddressBook(UserDict):
    def add_contact(self, contact: Contact):
        self.data[contact.name.value] = contact

    def get_contact(self, name: str):
        return self.data.get(name)

    def delete_contact(self, name: str):
        if name in self.data:
            del self.data[name]

    def find_contacts(self, keyword: str):
        return [c for c in self.data.values() if keyword.lower() in c.name.value.lower()]

    def upcoming_birthdays(self, days: int):
        today = datetime.now().date()
        result = []
        for contact in self.data.values():
            if contact.birthday:
                try:
                    bday = datetime.strptime(contact.birthday.value, "%d.%m.%Y").date()
                    bday_this_year = bday.replace(year=today.year)
                    delta = (bday_this_year - today).days
                    if 0 <= delta <= days:
                        result.append(contact)
                except ValueError:
                    continue
        return result

# ------------------ Help Commands ------------------
def show_contacts_help():
    print(Fore.CYAN + "Available commands:" + Style.RESET_ALL)
    commands = (
        Fore.GREEN +
        "  add        - add new contact\n"
        "  edit       - edit existing contact\n"
        "  delete     - delete contact\n"
        "  search     - search contacts\n"
        "  all        - show all contacts\n"
        "  birthdays  - show upcoming birthdays\n"
        "  help       - show this help message\n"
        "  back       - return to main menu" +
        Style.RESET_ALL
    )
    print(commands)
