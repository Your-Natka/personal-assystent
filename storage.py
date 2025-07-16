import pickle
import os
from Address_book.address_book import AddressBook
from Address_book.record import Record
from datetime import datetime, timedelta

# Ініціалізація адресної книги
contacts = AddressBook()
data_file = "addressbook.pkl"

def get_upcoming_birthdays(days=7):
    today = datetime.today().date()
    upcoming = []

    for name, record in contacts.data.items():
        if not record.birthday:
            continue

        bday = record.birthday.value
        # Перестворити дату народження для поточного року
        next_birthday = bday.replace(year=today.year)

        # Якщо вже пройшов — дивимось на наступний рік
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)

        delta = (next_birthday - today).days

        if 0 <= delta <= days:
            upcoming.append(f"{name} — {next_birthday.strftime('%d.%m')} (через {delta} дн.)")

    if not upcoming:
        return ["Немає днів народження найближчим часом."]
    return upcoming



def set_data_directory(directory):
    global data_file
    data_file = os.path.join(directory, "addressbook.pkl")
    load_data()

def save_data():
    with open(data_file, "wb") as f:
        pickle.dump(contacts, f)

def load_data():
    global contacts
    if os.path.exists(data_file):
        with open(data_file, "rb") as f:
            contacts = pickle.load(f)

def add_contact(name, phone):
    record = contacts.find(name)
    if not record:
        record = Record(name)
        contacts.add_record(record)
    record.add_phone(phone)
    save_data()
    return f"Contact '{name}' updated successfully."

def change_contact(name, new_phone):
    record = contacts.find(name)
    if record:
        record.phones = [new_phone]
        save_data()
        return f"Phone number for '{name}' changed to {new_phone}"
    return f"Contact '{name}' not found."

def add_full_contact(name, phone, email, address, birthday):
    record = contacts.find(name)
    if record:
        return f"Contact '{name}' already exists."
    record = Record(name)
    record.add_phone(phone)
    record.email = email
    record.address = address
    record.set_birthday(birthday)
    contacts.add_record(record)
    save_data()
    return f"Full contact '{name}' added."

def edit_contact(name, phone=None, email=None, address=None, birthday=None):
    record = contacts.find(name)
    if not record:
        return f"Contact '{name}' not found."

    if phone:
        record.phones = [phone]
    if email:
        record.email = email
    if address:
        record.address = address
    if birthday:
        record.set_birthday(birthday)

    save_data()
    return f"Contact '{name}' updated successfully."

def edit_email(name, new_email):
    record = contacts.find(name)
    if record:
        record.email = new_email
        save_data()
        return f"Email for '{name}' updated."
    return f"Contact '{name}' not found."

def edit_address(name, new_address):
    record = contacts.find(name)
    if record:
        record.address = new_address
        save_data()
        return f"Address for '{name}' updated."
    return f"Contact '{name}' not found."

def show_phone(name):
    record = contacts.find(name)
    if record:
        return f"{name}'s phone(s): {', '.join(str(p) for p in record.phones)}"
    return f"Contact '{name}' not found."

def show_contact(name):
    record = contacts.find(name)
    if not record:
        return f"Contact '{name}' not found."
    phones = ', '.join(str(p) for p in record.phones)
    birthday = record.birthday.strftime('%d.%m.%Y') if record.birthday else 'N/A'
    email = record.email if record.email else 'N/A'
    address = record.address if record.address else 'N/A'
    return (
        f"Contact name: {name}, phones: {phones}, "
        f"birthday: {birthday}, email: {email}, address: {address}"
    )

def show_all():
    if not contacts:
        return ["No contacts found."]

    result = []
    for name, record in contacts.data.items():
        result.append(str(record))
    return result


def add_birthday(name, birthday):
    record = contacts.find(name)
    if record:
        record.set_birthday(birthday)
        save_data()
        return f"{name}'s birthday is {birthday}."
    return f"Contact '{name}' not found."

def show_birthday(name):
    record = contacts.find(name)
    if record and record.birthday:
        return f"{name}'s birthday is {record.birthday.strftime('%d.%m.%Y')}"
    return f"Birthday for '{name}' not found."

def birthdays():
    upcoming = contacts.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    return "\n".join(upcoming)

def delete_contact(name):
    if name in contacts.data:
        del contacts.data[name]
        save_data()
        return f"Contact '{name}' deleted."
    return f"Contact '{name}' not found."
