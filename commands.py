from difflib import get_close_matches
from data import contacts
from storage import (
    add_contact_interactive, edit_contact_interactive,
    delete_contact, show_all, show_contact, save_data, search, add_note_interactive,
    edit_note_interactive,
    save_notes, load_notes, delete_note ,show_notes, find_note
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

        # elif command == "show-birthday":
        #     if len(args) != 1:
        #         return "Invalid command. Use: show-birthday [username]"
        #     return show_birthday(args[0])
        
        elif command == "birthdays":
            return "\n".join(contacts.get_upcoming_birthdays(7))
        
        elif command == "birthdays-in":
            if not args or not args[0].isdigit():
                return "Please specify number of days. Example: birthdays-in 7"
            days = int(args[0])
            return "\n".join(contacts.get_upcoming_birthdays(days))

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
        
        elif command == "find-note":
            if args:
                return find_note(args.strip())
            else:
                return "Please provide a keyword to search for notes."

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