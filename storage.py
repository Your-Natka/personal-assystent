from error_handlers import input_error
from contacts.record import Record 
from datetime import datetime
import os
import pickle
from contacts.book import AddressBook
from notebook.notes import Notebook
from contacts.fields import Birthday, Email, Address

# Початковий шлях до файлу
DATA_DIRECTORY = "."
DATA_FILE = "contacts.pkl"
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
        record.add_phone(phone)
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
def edit_contact_interactive():
    print("Editing contact (type 'exit' to cancel or press Enter to skip a field)")

    name = input("Enter the name of the contact you want to edit: ").strip()
    if name.lower() == 'exit':
        return "Cancelled."

    if name not in contacts:
        return f"Contact '{name}' not found."

    record = contacts[name]

    # Phone
    current_phone = ", ".join(str(p) for p in record.phones) or "None"
    print(f"Current phone(s): {current_phone}")
    new_phone = input("Enter new phone (or press Enter to keep current): ").strip()
    if new_phone.lower() == 'exit':
        return "Cancelled."
    if new_phone:
        record.phones.clear()
        record.add_phone(new_phone)

    # Email
    current_email = str(record.email) if record.email else "None"
    print(f"Current email: {current_email}")
    new_email = input("Enter new email (or press Enter to keep current): ").strip()
    if new_email.lower() == 'exit':
        return "Cancelled."
    if new_email:
        record.add_email(new_email)

    # Address
    current_address = str(record.address) if record.address else "None"
    print(f"Current address: {current_address}")
    new_address = input("Enter new address (or press Enter to keep current): ").strip()
    if new_address.lower() == 'exit':
        return "Cancelled."
    if new_address:
        record.add_address(new_address)

    # Birthday
    current_birthday = str(record.birthday) if record.birthday else "None"
    print(f"Current birthday: {current_birthday}")
    new_birthday = input("Enter new birthday (DD.MM.YYYY) (or press Enter to keep current): ").strip()
    if new_birthday.lower() == 'exit':
        return "Cancelled."
    if new_birthday:
        try:
            record.add_birthday(new_birthday)
        except ValueError as e:
            print(f"Invalid birthday format: {e}")

    return f"Contact '{name}' updated successfully."

@input_error
def search(keyword):
    """
    Шукає контакти за ім'ям, телефоном, email, адресою або днем народження.
    """
    keyword = keyword.lower()
    results = []

    for name, record in contacts.data.items():
        # Ім’я
        if keyword in name.lower():
            results.append(str(record))
            continue

        # Телефони
        for phone in record.phones:
            if keyword in phone.value:
                results.append(str(record))
                break

        # Email
        if record.email and keyword in record.email.value.lower():
            results.append(str(record))
            continue

        # Адреса
        if record.address and keyword in record.address.value.lower():
            results.append(str(record))
            continue

        # День народження
        if record.birthday and keyword in record.birthday.value.strftime("%d.%m.%Y"):
            results.append(str(record))
            continue

    if not results:
        return "No matching contacts found."

    return "\n\n".join(results)

# @input_error
# def edit_email(name, new_email):
#     """
#     Редагує email для існуючого контакту.
#     """
#     record = contacts.find(name)
#     if not record:
#         return f"Contact '{name}' not found."
#     record.edit_email(new_email)
#     return f"Email for contact '{name}' updated to: {new_email}"

# @input_error
# def edit_address(name, new_address):
#     """
#     Редагує адресу для існуючого контакту.
#     """
#     record = contacts.find(name)
#     if not record:
#         return f"Contact '{name}' not found."
#     record.edit_address(new_address)
#     return f"Address for contact '{name}' updated to: {new_address}"

# @input_error
# def change_contact(name, new_phone):
#     """
#     Змінює існуючий контакт.
#     """
#     record = contacts.find(name)
#     if not record:
#         return f"Contact '{name}' not found."
#     if not record.phones:
#         return f"Contact '{name}' has no phone numbers to change."
    
#     old_phone = record.phones[0].value
#     record.edit_phone(old_phone, new_phone)
#     return f"Contact '{name}' updated: '{old_phone}' → '{new_phone}'."

@input_error
def show_contact(name):
    """
    Показує контакт за іменем.
    """
    record = contacts.find(name)
    if record:
        return str(record)
    return f"Contact '{name}' not found."

# @input_error

# def show_phone(name):
#     """
#     Виводить номер телефону для вказаного імені.
#     """
#     record = contacts.find(name)
#     if record:
#         return ", ".join(p.value for p in record.phones) if record.phones else "No phones"
#     return f"Contact '{name}' not found."

# @input_error
# def add_birthday(name, bday_str):
#     """
#     Додає день народження до контакту.
#     """
#     record = contacts.find(name)
#     if not record:
#         return f"Contact '{name}' not found."
#     try:
#         record.add_birthday(bday_str)
#         return f"Birthday added to contact '{name}': {bday_str}"
#     except ValueError as e:
#         return str(e)

# @input_error
# def show_birthday(name):
#     """
#     Показує день народження контакту.
#     """
#     record = contacts.find(name)
#     if not record:
#         return f"Contact '{name}' not found."
#     if record.birthday:
#         return f"{name}'s birthday is {record.birthday.value.strftime('%d.%m.%Y')}"
#     else:
#         return f"No birthday set for contact '{name}'."

@input_error
def birthdays(days: int):
    result = contacts.get_upcoming_birthdays(days)
    return result if result else ["Немає днів народження найближчим часом."]

@input_error
def birthdays_in(days: int):
    try:
        days = int(days)
        upcoming = contacts.get_upcoming_birthdays(days)
        if not upcoming:
            return f"No birthdays in the next {days} days."
        else:
            return f"Birthdays in the next {days} days:\n" + "\n".join(upcoming)
    except ValueError:
        return "Please provide a valid number of days."

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


@input_error
def add_note_interactive():
    print('Adding a new note (type ‘exit’ to cancel at any time)')
    text = input('Enter the text of the note: ').strip()
    if not text or text.lower() == 'exit':
        return 'Cancelled.'
    tags_input = input('Enter tags (comma-separated, optional): ').strip().split(',')
    if tags_input.lower() == 'exit':
        return 'Cancelled.'
    tags = [tag.strip() for tag in tags_input if tag.strip()] if tags_input else []
    notebook.add_note(text, tags)
    save_notes(notebook)
    return f"Note added successfully:\nNote(text='{text}', tags={tags})"

# Додавання нової нотатки з тегами
# def add_note(notes: NoteBook):
#     print(Fore.GREEN + "\n+ Додавання нової нотатки (натисніть Enter для скасування)")
#     text = input("Введіть текст нотатки: ").strip()
#     if not text:
#         print(Fore.YELLOW + "Додавання скасовано.")
#         return
#     tags = input("Введіть теги (через кому) або натисніть Enter для пропуску: ").strip().split(',')
#     tags = [t.strip() for t in tags if t.strip()] if tags else []
#     note = Note(text=text, tags=tags)
#     notes.add_note(note)
#     save_data(None, notes)  # Зберігаємо лише нотатки
#     print(Fore.GREEN + "✓ Нотатку додано успішно!")


@input_error
def edit_note_interactive():
    print('Editing a note (type ‘exit’ to cancel or press Enter to skip a field)')
    if not notebook.notes:
        return "No notes available to edit."
    # Показуємо всі нотатки
    print("\nAvailable notes:")
    for idx, note in enumerate(notebook.notes, 1):
        tags_str = ", ".join(note.tags) if note.tags else "no tags"
        print(f"{idx}. {note.text} [{tags_str}]")
    note_index_input = input("\nEnter the number of the note to edit: ").strip()
    if note_index_input.lower() == 'exit':
        return "Cancelled."
    if not note_index_input.isdigit():
        return "Invalid input. Please enter a number."
    note_index = int(note_index_input) - 1
    if note_index < 0 or note_index >= len(notebook.notes):
        return "Invalid note number."
    note = notebook.notes[note_index]
    print(f"\nCurrent text: {note.text}")
    new_text = input("Enter new text (or press Enter to keep current): ").strip()
    if new_text.lower() == 'exit':
        return "Cancelled."
    if new_text:
        note.text = new_text
    current_tags = ", ".join(note.tags) if note.tags else "None"
    print(f"Current tags: {current_tags}")
    new_tags_input = input("Enter new tags (comma-separated) (or press Enter to keep current): ").strip()
    if new_tags_input.lower() == 'exit':
        return "Cancelled."
    if new_tags_input:
        note.tags = [tag.strip() for tag in new_tags_input.split(",") if tag.strip()]
    save_notes(notebook)
    return f"Note updated successfully:\n{note}"

