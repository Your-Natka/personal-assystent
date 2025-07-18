import os
import pickle
from contacts.book import AddressBook

# Шлях до файлу збереження
DATA_FILE = os.path.join(os.getcwd(), "contacts.bin")

# Функція для завантаження книги з диска
def load_data(filename=DATA_FILE):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    return AddressBook()

# Глобальний об'єкт адресної книги
contacts = load_data()