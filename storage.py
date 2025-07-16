from error_handlers import input_error
from address_book.record import Record 
from datetime import datetime
import os
import pickle
from address_book.book import AddressBook
from notebook.notes import Notebook
from address_book.fields import Birthday, Phone, Email, Address

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

def save_data(book: AddressBook):
    with open((get_data_path()), "wb") as f:
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
def add_contact_interactive():
    print("Adding new contact (press Enter to skip a field or type 'exit' to cancel)")

    def ask_field(prompt):
        value = input(prompt).strip()
        if value.lower() == 'exit':
            return None, True  # скасування
        return value, False

    def ask_continue():
        while True:
            cont = input("Do you want to continue? (yes/no): ").strip().lower()
            if cont in ('yes', 'y'):
                return True
            elif cont in ('no', 'n'):
                return False
            else:
                print("Please answer 'yes' or 'no'.")

    # Ім'я (обов'язкове)
    while True:
        name, cancel = ask_field("Enter name: ")
        if cancel:
            return "Cancelled."
        if not name:
            print("Name is required.")
        elif name in contacts:
            return f"Contact '{name}' already exists."
        else:
            break

    record = Record(name)

    # Телефон (опціонально)
    phone, cancel = ask_field("Enter phone (optional): ")
    if cancel:
        return "Cancelled."
    if phone:
        record.add_phone(Phone(phone))
    if phone and not ask_continue():
        contacts.add_record(record)
        return f"Contact '{name}' added successfully."

    # Email (опціонально)
    email, cancel = ask_field("Enter email (optional): ")
    if cancel:
        return "Cancelled."
    if email:
        record.email = Email(email)
    if email and not ask_continue():
        contacts.add_record(record)
        return f"Contact '{name}' added successfully."

    # Адреса (опціонально)
    address, cancel = ask_field("Enter address (optional): ")
    if cancel:
        return "Cancelled."
    if address:
        record.address = Address(address)
    if address and not ask_continue():
        contacts.add_record(record)
        return f"Contact '{name}' added successfully."

    # День народження (опціонально)
    birthday, cancel = ask_field("Enter birthday (DD.MM.YYYY, optional): ")
    if cancel:
        return "Cancelled."
    if birthday:
        try:
            record.birthday = Birthday(birthday)
        except ValueError as e:
            return f"Invalid birthday format: {e}"

    contacts.add_record(record)
    return f"Contact '{name}' added successfully."

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
    if record:
        return str(record)
    return f"Contact '{name}' not found."

@input_error

def show_phone(name):
    """
    Виводить номер телефону для вказаного імені.
    """
    record = contacts.find(name)
    if record:
        return ", ".join(p.value for p in record.phones) if record.phones else "No phones"
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
    Виводить усі контакти та поля в зручному для читання форматі.
    """
    if not contacts.data:
        return "No contacts found."

    result = ""
    for name, record in contacts.data.items():
        lines = [f"Name: {name}"]
        if record.phones:
            lines.append("Phones: " + ", ".join(p.value for p in record.phones))
        if record.email:
            lines.append(f"Email: {record.email.value}")
        if record.address:
            lines.append(f"Address: {record.address.value}")
        if record.birthday:
            lines.append(f"Birthday: {record.birthday.value.strftime('%d.%m.%Y')}")
        result += "\n".join(lines) + "\n" + "-"*30 + "\n"
    return result.strip()