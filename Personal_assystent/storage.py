from error_handlers import input_error
from Address_book.address_book import AddressBook
from Address_book.record import Record, Birthday
from datetime import datetime
from Address_book.fields import Phone
import pickle
import os

DATA_FILE = "addressbook.pkl"

def save_data(book: AddressBook, filename=DATA_FILE):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename=DATA_FILE) -> AddressBook:
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    return AddressBook()

contacts = load_data()

@input_error
def add_contact(name, phone):
    """
    Додає новий контакт.
    """
    record = Record(name)
    record.add_phone(phone)
    contacts.add_record(record)
    return f"Contact '{name}' added with phone '{phone}'."

@input_error
def change_contact(name, new_phone):
    """
    Змінює існуючий контакт.
    """
    record = contacts.find(name)
    if not record:
        return f"Contact '{name}' not found."
    if not record.phones:
        return f"Contact '{name}' has no phone numbers to change."
    
    old_phone = record.phones[0].value
    record.edit_phone(old_phone, new_phone)
    return f"Contact '{name}' updated: '{old_phone}' → '{new_phone}'."


@input_error
def show_phone(name):
    """
    Виводить номер телефону для вказаного імені.
    """
    record = contacts.find(name)
    if record:
        return str(record)
    return f"Contact '{name}' not found."

@input_error
def add_birthday(name, bday_str):
    """
    Додає день народження до контакту.
    """
    record = contacts.find(name)
    if not record:
        return f"Contact '{name}' not found."
    try:
        record.add_birthday(bday_str)
        return f"Birthday added to contact '{name}': {bday_str}"
    except ValueError as e:
        return str(e)

@input_error
def show_birthday(name):
    """
    Показує день народження контакту.
    """
    record = contacts.find(name)
    if not record:
        return f"Contact '{name}' not found."
    if record.birthday:
        return f"{name}'s birthday is {record.birthday.value.strftime('%d.%m.%Y')}"
    else:
        return f"No birthday set for contact '{name}'."

@input_error
def birthdays():
    """
    Показує список користувачів, яких потрібно привітати наступного тижня.
    """
    upcoming = contacts.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays in the upcoming week."
    return "\n".join(upcoming)

@input_error
def delete_contact(name):
    """
    Видаляє контакт із книги.
    """
    try:
        contacts.delete(name)
        return f"Contact '{name}' deleted successfully."
    except KeyError:
        return f"Contact '{name}' not found."
    
@input_error
def show_all():
    """
    Виводить усі контакти та номери телефонів.
    """
    if not contacts.data:
        return "No contacts found."
    return str(contacts)