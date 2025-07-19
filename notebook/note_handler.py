# логіка обробки нотаток
from colorama import Fore, Style
from notebook.notes import Note, NoteBook
from data.storage import save_data

# Додавання нової нотатки з тегами
def add_note(notes: NoteBook):
    print(Fore.GREEN + "\n+ Додавання нової нотатки (натисніть Enter для скасування)")
    
    text = input("Введіть текст нотатки: ").strip()
    if not text:
        print(Fore.YELLOW + "Додавання скасовано.")
        return

    tags = input("Введіть теги (через кому) або натисніть Enter для пропуску: ").strip().split(',')
    tags = [t.strip() for t in tags if t.strip()] if tags else []

    note = Note(text=text, tags=tags)
    notes.add_note(note)
    save_data(None, notes)  # Зберігаємо лише нотатки
    print(Fore.GREEN + "✓ Нотатку додано успішно!")

# Виведення всіх нотаток
def show_notes(notes: NoteBook):
    print(Fore.CYAN + "\nВсі нотатки:")
    for idx, note in enumerate(notes.list_notes(), start=1):
        print(f"{idx}. {note}")
    if not notes.notes:
        print("Нотаток не знайдено.")

# Пошук нотаток за ключовим словом або тегом
def find_note(notes: NoteBook):
    keyword = input("Введіть ключове слово для пошуку в нотатках: ").strip()
    results = notes.find_notes(keyword)
    if results:
        print(Fore.CYAN + "\nЗнайдено нотатки:")
        for idx, note in enumerate(results, start=1):
            print(f"{idx}. {note}")
    else:
        print(Fore.YELLOW + "Немає нотаток, що відповідають запиту.")

# Редагування існуючої нотатки
def edit_note(notes: NoteBook):
    show_notes(notes)  # Показуємо всі нотатки для вибору
    try:
        index = int(input("Введіть індекс нотатки для редагування: ")) - 1
        new_text = input("Введіть новий текст або натисніть Enter для збереження поточного: ").strip()
        new_tags = input("Введіть нові теги (через кому) або натисніть Enter: ").strip()
        tags = [t.strip() for t in new_tags.split(',')] if new_tags else None

        notes.edit_note(index, new_text or None, tags)
        save_data(None, notes)
        print(Fore.GREEN + "✓ Нотатку успішно оновлено.")
    except (ValueError, IndexError):
        print(Fore.RED + "✗ Неправильний індекс або введення.")

# Видалення нотатки за індексом
def delete_note(notes: NoteBook):
    show_notes(notes)
    try:
        index = int(input("Введіть індекс нотатки для видалення: ")) - 1
        notes.delete_note(index)
        save_data(None, notes)
        print(Fore.GREEN + "✓ Нотатку видалено успішно.")
    except (ValueError, IndexError):
        print(Fore.RED + "✗ Неправильний індекс.")

# ------------------ Help Commands ------------------
def show_notes_help():
    print(Fore.CYAN + "Available commands:" + Style.RESET_ALL)
    commands = (
        Fore.GREEN +
        "  add          - add a note with tags\n"
        "  all          - show all notes\n"
        "  find         - find notes by keyword\n"
        "  edit         - edit note by index\n"
        "  delete       - delete note by index\n"
        "  help         - show this help message\n"
        "  back         - return to main menu" +
        Style.RESET_ALL
    )
    print(commands)

