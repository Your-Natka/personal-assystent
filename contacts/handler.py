from colorama import Fore
from address_book.models import Contact, Phone, Email, Address, Birthday
from data.storage import save_data

# Додавання нового контакту

def add_contact(book):
    print(Fore.GREEN + "\n+ Додавання нового контакту (або натисніть Enter для скасування)")

    name = input("Введіть ім'я: ").strip()
    if not name:
        print(Fore.YELLOW + "Додавання скасовано.")
        return

    # Отримання номерів телефону
    phones = input("Введіть номери телефону (10 цифр, через кому), або натисніть Enter для пропуску: ").split(',')
    phones = [p.strip() for p in phones if p.strip()] if phones else []

    email = input("Введіть email або натисніть Enter для пропуску: ").strip() or None
    address = input("Введіть адресу або натисніть Enter для пропуску: ").strip() or None
    birthday = input("Введіть дату народження (ДД.ММ.РРРР) або натисніть Enter для пропуску: ").strip() or None

    try:
        # Створення об'єкта контакту та додавання до книги
        contact = Contact(name=name, phones=phones, email=email, address=address, birthday=birthday)
        book.add_contact(contact)
        save_data(book, None)  # Збереження тільки книги контактів
        print(Fore.GREEN + "\n✅ Контакт успішно додано!")
    except ValueError as e:
        print(Fore.RED + f"\n❌ Помилка: {e}")

# Редагування існуючого контакту

def edit_contact(book):
    name = input("Введіть ім'я контакту для редагування: ").strip()
    contact = book.get_contact(name)
    if not contact:
        print(Fore.RED + "Контакт не знайдено.")
        return

    print(Fore.YELLOW + f"Редагування {name} (залиште поле порожнім, щоб зберегти поточне значення)")

    new_phones = input("Нові телефони (через кому): ").strip()
    if new_phones:
        contact.phones = [Phone(p.strip()) for p in new_phones.split(',')]

    new_email = input("Новий email: ").strip()
    if new_email:
        contact.email = Email(new_email)

    new_address = input("Нова адреса: ").strip()
    if new_address:
        contact.address = Address(new_address)

    new_bday = input("Нова дата народження (ДД.ММ.РРРР): ").strip()
    if new_bday:
        contact.birthday = Birthday(new_bday)

    save_data(book, None)  # Збереження книги контактів
    print(Fore.GREEN + "✅ Контакт оновлено.")

# Видалення контакту

def delete_contact(book):
    name = input("Введіть ім'я контакту для видалення: ").strip()
    if book.get_contact(name):
        book.delete_contact(name)
        save_data(book, None)
        print(Fore.GREEN + "✅ Контакт видалено.")
    else:
        print(Fore.RED + "❌ Контакт не знайдено.")

# Пошук контактів за ключовим словом

def search_contacts(book):
    keyword = input("Введіть ключове слово для пошуку: ").strip()
    results = book.find_contacts(keyword)
    if results:
        print(Fore.CYAN + f"\n🔍 Знайдено {len(results)} контакт(ів):")
        for contact in results:
            print(contact)
    else:
        print(Fore.YELLOW + "Контактів не знайдено.")

# Виведення всіх контактів

def show_all_contacts(book):
    if not book.data:
        print(Fore.YELLOW + "Немає контактів для відображення.")
    else:
        for contact in book.data.values():
            print(contact)

# Пошук днів народження, що наближаються

def birthdays_reminder(book):
    try:
        days = int(input("Введіть кількість днів: "))
        results = book.upcoming_birthdays(days)
        if results:
            print(Fore.CYAN + f"Дні народження в межах {days} днів:")
            for c in results:
                print(c)
        else:
            print(Fore.YELLOW + "Немає днів народження в заданий період.")
    except ValueError:
        print(Fore.RED + "Некоректне число.")