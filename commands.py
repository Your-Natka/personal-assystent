from difflib import get_close_matches
from data import contacts
from storage import (
    add_contact_interactive, edit_contact_interactive,
    delete_contact, show_all, show_birthday, birthdays,
    show_contact, save_data, search,
    save_notes, load_notes, get_upcoming_birthdays
)

notebook = load_notes()

ALL_COMMANDS = [
    "hello", "help", "add", "edit", "show", "search",
    "birthdays", "birthdays-in", "delete", "all",
    "add-note", "show-notes", "find-note", "edit-note", "delete-note"
]

def suggest_command(user_input):
    suggestion = get_close_matches(user_input, ALL_COMMANDS, n=1)
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
                "show-birthday  - show birthday of contact\n"
                "birthdays      - show upcoming birthdays\n"
                "birthdays-in   - show birthdays in given days\n"
                "delete         - delete contact\n"
                "all            - show all contacts\n"
                "add-note       - add a note with tags\n"
                "show-notes     - show all notes\n"
                "find-note      - find notes by keyword\n"
                "edit-note      - edit note by index\n"
                "delete-note    - delete note by index\n"
                "help           - show this help message\n"
            )

        elif command == "add":
            result = add_contact_interactive()
            save_data(contacts)
            return result

        elif command in ["edit", "edit-contact"]:
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

        elif command == "show-birthday":
            if len(args) != 1:
                return "Invalid command. Use: show-birthday [username]"
            return show_birthday(args[0])

        elif command == "birthdays":
            return birthdays()

        elif command == "birthdays-in":
            if not args or not args[0].isdigit():
                return "Please specify number of days. Example: birthdays-in 7"
            days = int(args[0])
            return "\n".join(get_upcoming_birthdays(days))

        elif command == "search":
            if not args:
                return "Invalid command. Use: search [keyword]"
            return search(" ".join(args))

        elif command == "all":
            return show_all()

        elif command == "add-note":
            if len(args) < 2:
                return "Invalid command. Use: add-note [text] [tag1,tag2,...]"
            text = " ".join(args[:-1])
            tags = args[-1].split(',')
            result = notebook.add_note(text, tags)
            save_notes(notebook)
            return result

        elif command == "show-notes":
            return "\n".join(notebook.list_notes()) or "No notes yet."

        elif command == "find-note":
            if not args:
                return "Invalid command. Use: find-note [keyword]"
            result = notebook.find_notes(" ".join(args))
            return "\n".join(str(n) for n in result) or "No matching notes found."

        elif command == "edit-note":
            if len(args) < 2:
                return "Invalid command. Use: edit-note [index] [new text] [new_tag1,new_tag2,...]"
            index = int(args[0])
            text = args[1]
            tags = args[2].split(",") if len(args) > 2 else None
            result = notebook.edit_note(index, text, tags)
            save_notes(notebook)
            return result

        elif command == "delete-note":
            if not args:
                return "Invalid command. Use: delete-note [index]"
            index = int(args[0])
            result = notebook.remove_note(index)
            save_notes(notebook)
            return result

        else:
            suggestion = suggest_command(command)
            if suggestion:
                return f"Unknown command '{command}'. Did you mean: '{suggestion}'?"
            return "Invalid command. Please try again."

    except Exception as e:
        return f"An error occurred: {e}"
