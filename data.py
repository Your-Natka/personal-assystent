import os
import pickle
from contacts.book import AddressBook
from notebook.notes import Note

# Шляхи до файлів
DATA_FILE = os.path.join(os.getcwd(), "contacts.bin")
NOTES_FILE = os.path.join(os.getcwd(), "notes.pkl")

# Завантаження контактів
def load_data(filename=DATA_FILE):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    return AddressBook()

# Збереження контактів
def save_data(address_book, filename=DATA_FILE):
    with open(filename, "wb") as f:
        pickle.dump(address_book, f)

# Завантаження нотаток
def load_notes(filename=NOTES_FILE):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    return []

# Збереження нотаток
def save_notes(notes, filename=NOTES_FILE):
    with open(filename, "wb") as f:
        pickle.dump(notes, f)

# Глобальні змінні
contacts = load_data()
notes_data = load_notes()
