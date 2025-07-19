from colorama import init, Fore, Style
from difflib import get_close_matches                # ✅ Для інтелектуального аналізу команд
from data.storage import load_data, save_data
from address_book import (
    add_contact, edit_contact, delete_contact,
    search_contacts, show_all_contacts,
    birthdays_reminder, show_contacts_help
)
from notebook import (
    add_note,
    delete_note,
    edit_note,
    show_notes,
    find_note as search_notes,
    show_notes_help
)

# Ініціалізація colorama для коректного відображення кольорів у Windows
init(autoreset=True)

def contacts_help():
    print(Fore.MAGENTA + "Available commands:" + Style.RESET_ALL)
    print(
    Fore.GREEN +
        "add            - add new contact\n"
        "edit           - edit existing contact\n"
        "delete         - delete contact\n"
        "search         - search contacts\n"
        "all            - show all contacts\n"
        "birthdays      - show upcoming birthdays\n"
        "birthdays-in   - show birthdays in given days\n"
        "help           - show this help message\n"
        "back           - return to main menu" +
        Style.RESET_ALL
    )

def notes_help():
    print(Fore.MAGENTA + "Available commands:" + Style.RESET_ALL)
    print(
    Fore.GREEN +
        "add-note    - add a note with tags\n"
        "show-notes  - show all notes\n"
        "find-note   - find notes by keyword\n"
        "edit-note   - edit note by index\n"
        "delete-note - delete note by index\n"
        "help        - show this help message\n"
        "back        - return to main menu" +
        Style.RESET_ALL
    )

def main(directory=None):
    print(Fore.BLUE + "Welcome to the assistant bot!" + Style.RESET_ALL)

    if directory:
        if not os.path.exists(directory):
            os.makedirs(directory)
        set_data_directory(directory)

    while True:
        user_input = input(Fore.CYAN + "Enter command: ").strip().lower()

        if user_input == "back":
            print(Fore.BLUE + "↩️  Returning to main menu.")
            break
        elif user_input == "add":
            add_contact(book)
        elif user_input == "edit":
            edit_contact(book)
        elif user_input == "delete":
            delete_contact(book)
        elif user_input == "search":
            search_contacts(book)
        elif user_input == "all":
            show_all_contacts(book)
        elif user_input == "birthdays":
            birthdays_reminder(book)
        elif user_input == "help":
            show_contacts_help()
        else:
            suggestion = suggest_command(user_input, valid_commands)
            if suggestion:
                print(Fore.YELLOW + f"❓ Можливо ви мали на увазі '{suggestion}'?")
            else:
                print(Fore.RED + "❌ Unknown command. Type 'help' to see available commands.")

def notes_mode(book, notes):
    print(Fore.YELLOW + "\n📓 Entering notes mode " + Style.DIM + "(type 'help' for available commands)")
    valid_commands = ['add', 'edit', 'delete', 'list', 'search', 'help', 'back']
    while True:
        user_input = input(Fore.CYAN + "Enter command: ").strip().lower()

        if user_input == "back":
            print(Fore.BLUE + "↩️  Returning to main menu.")
            break
        elif user_input == "add":
            add_note(notes)
        elif user_input == "edit":
            edit_note(notes)
        elif user_input == "delete":
            delete_note(notes)
        elif user_input == "all":
            show_notes(notes)
        elif user_input == "find":
            search_notes(notes)
        elif user_input == "help":
            show_notes_help()
        else:
            suggestion = suggest_command(user_input, valid_commands)
            if suggestion:
                print(Fore.YELLOW + f"❓ Можливо ви мали на увазі '{suggestion}'?")
            else:
                print(Fore.RED + "❌ Unknown command. Type 'help' to see available commands.")

def main():
    book, notes = load_data()
    print(Fore.GREEN + "👋 Welcome to Personal Assistant!")
    while True:
        mode = input(Fore.CYAN + "\nEnter mode (contacts/notes or exit): ").strip().lower()

        if mode == "contacts":
            contacts_mode(book, notes)
        elif mode == "notes":
            notes_mode(book, notes)
        elif mode == "exit":
            print(Fore.GREEN + "👋 Good bye!")
            save_data(book, notes)
            break
        else:
            suggestion = suggest_command(mode, ['contacts', 'notes', 'exit'])
            if suggestion:
                print(Fore.YELLOW + f"❓ Можливо ви мали на увазі '{suggestion}'?")
            else:
                print(Fore.RED + "❌ Invalid input. Please enter 'contacts', 'notes' or 'exit'.")

if __name__ == "__main__":
    main()
