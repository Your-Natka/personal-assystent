from error_handlers import input_error
from Address_book.record import Record 
from datetime import datetime
import os
import pickle
from Address_book.address_book import AddressBook
from Address_book.notes import Notebook

# Початковий шлях до файлу
DATA_DIRECTORY = "."
DATA_FILE = "addressbook.pkl"
NOTEBOOK_FILE = "notes_data.pkl"

def set_data_directory(directory):
    global DATA_DIRECTORY
    DATA_DIRECTORY = directory

def get_data_path():
    return os.path.join(DATA_DIRECTORY, DATA_FILE)

def get_notes_path():
    return os.path.join(DATA_DIRECTORY, NOTEBOOK_FILE)

def save_data(book: AddressBook, filename=DATA_FILE):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(book: AddressBook):
    with open(get_data_path(), "wb") as f:
        pickle.dump(book, f)

def load_data() -> AddressBook:
    if os.path.exists(get_data_path()):
        with open(get_data_path(), "rb") as f:
            return pickle.load(f)
    return AddressBook()
# Initialize the address book and notebook
contacts = load_data()

def save_notes(notebook):
    with open(get_notes_path(), "wb") as f:
        pickle.dump(notebook, f)

def load_notes():
    try:
        with open(get_notes_path(), "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return Notebook()
notebook = load_notes()

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
def add_full_contact(name, phone, email, address, birthday):
    """
    Додає контакт з повною інформацією.
    """
    if name in contacts:
        return f"Contact '{name}' already exists."
    
    record = Record(name)
    record.add_phone(phone)
    record.add_email(email)
    record.add_address(address)
    if birthday:
        record.add_birthday(birthday)
    contacts[name] = record
    return f"Full contact '{name}' додано."


@input_error
def edit_email(name, new_email):
    """
    Редагує email для існуючого контакту.
    """
    record = contacts.find(name)
    if not record:
        return f"Contact '{name}' not found."
    record.edit_email(new_email)
    return f"Email for contact '{name}' updated to: {new_email}"

@input_error
def edit_address(name, new_address):
    """
    Редагує адресу для існуючого контакту.
    """
    record = contacts.find(name)
    if not record:
        return f"Contact '{name}' not found."
    record.edit_address(new_address)
    return f"Address for contact '{name}' updated to: {new_address}"

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
def show_contact(name):
    """
    Показує контакт за іменем.
    """
    record = contacts.find(name)
    if not record:
        return str(record)
    return f"Contact '{name}' not found."

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