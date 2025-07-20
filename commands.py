from difflib import get_close_matches
from data import contacts
from storage import (
    add_contact_interactive, edit_contact_interactive, sort_notes_by_first_tag,
    delete_contact, show_all, show_contact, save_data, search, add_note_interactive,
    edit_note_interactive, get_birthdays_in_days, load_notes, notes_data, delete_note, show_notes, find_note
)

notebook = load_notes()

ALL_COMMANDS = [
    "add-note", "show-notes", "find-note", "edit-note", "delete-note", "sort-notes",
    "add", "edit", "delete", "search", "all", "birthdays-in", "help", "back", "exit", "close", "hello"
]

command_aliases = {
    "add-note": ["додати", "нова нотатка", "створити нотатку"],
    "show-notes": ["показати", "всі нотатки", "нотатки"],
    "find-note": ["знайти", "пошук", "знайди"],
    "edit-note": ["редагувати", "змінити"],
    "delete-note": ["видалити", "стерти"],
    "sort-notes": ["сортувати", "відсортувати", "по тегам", "по тегах"],
}
ALLOWED_COMMANDS = ['add-note', 'show-notes', 'find-note', 'edit-note', 'delete-note', 'hello', 'help']

def suggest_command(user_input, allowed_commands=None):
    normalized = user_input.lower().strip()

    # Перевірка синонімів
    for command, aliases in command_aliases.items():
        if any(alias in normalized for alias in aliases):
            return command

    # Якщо allowed_commands задано, шукаємо серед них
    if allowed_commands:
        suggestion = get_close_matches(normalized, allowed_commands, n=1, cutoff=0.5)
    else:
        suggestion = get_close_matches(normalized, ALL_COMMANDS, n=1, cutoff=0.5)

    return suggestion[0] if suggestion else None

def execute_command(command, args):
    try:
        if command == "hello":
            return "How can I help you?"

        elif command == "help":
            return (
                "Available commands:\n"
                "add            - add new contact interactively\n"
                "edit           - edit contact's info (phone, email, address, birthday)\n"
                "show           - show contact info\n"
                "search         - search contacts by name\n"
                "birthdays-in   - show birthdays in given days\n"
                "delete         - delete contact\n"
                "all            - show all contacts\n"
                "add-note       - add a note with tags\n"
                "show-notes     - show all notes\n"
                "sort-notes     - sort notes by first tag\n"
                "find-note      - find notes by keyword\n"
                "edit-note      - edit note by index\n"
                "delete-note    - delete note by index\n"
                "help           - show this help message\n"
            )

        elif command == "add":
            result = add_contact_interactive()
            save_data(contacts)
            return result

        elif command in ["edit"]:
            result = edit_contact_interactive()
            save_data(contacts)
            return result

        elif command == "delete":
            if len(args) != 1:
                return "Invalid command. Use: delete [username]"
            result = delete_contact(args[0])
            save_data(contacts)
            return result

        elif command == "show":
            if len(args) != 1:
                return "Invalid command. Use: show [username]"
            return show_contact(args[0])
        
        elif command == "birthdays-in":
            if not args:
                return "Please provide the number of days. Usage: birthdays-in [days]"
            try:
                days = int(args[0])
                return get_birthdays_in_days(days)
            except ValueError:
                return "Please enter a valid number of days."
            
        elif command == "search":
            if not args:
                return "Invalid command. Use: search [keyword]"
            return search(" ".join(args))

        elif command == "all":
            return show_all()

        elif command == "add-note":
            return add_note_interactive()

        elif command == "edit-note":
            result = edit_note_interactive()
            return result
        
        elif command == "show-notes":
            return show_notes()
        
        elif command == "sort-notes":
            sorted_notes = notebook.sort_by_tags()
            return "\n\n".join(str(note) for note in sorted_notes) if sorted_notes else "No notes to show."

        if command == 'find-note':
            if not args:
                keyword = input("Please enter tag:\n> ").strip()
            else:
                keyword = ' '.join(args).strip()

            if keyword:  # Перевірка, що тег не порожній
                found = notebook.find_notes(keyword)
                if found:
                    return '\n\n'.join(str(note) for note in found)
                else:
                    return "No notes found with the tag."
            else:
                return "Tag cannot be empty."
        
        elif command == "delete-note":
            if args:
                try:
                    index = int(args[0])  # ✅ беремо перший елемент зі списку
                    return delete_note(index)
                except ValueError:
                    return "Invalid index. Please enter a number."
            else:
                return "Please provide the index of the note to delete."
            
        else:
            suggestion = suggest_command(command)
            if suggestion:
                return f"Unknown command '{command}'. Did you mean: '{suggestion}'?"
            return "Invalid command. Please try again."

    except Exception as e:
        return f"An error occurred: {e}"