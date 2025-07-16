from difflib import get_close_matches
from storage import (
    add_contact, change_contact, show_phone, show_all, add_birthday,
    show_birthday, birthdays, delete_contact, add_full_contact,
    edit_email, edit_address, show_contact, edit_contact
)
from notes import save_notes, load_notes  # ✅ Виправлено

ALL_COMMANDS = [
    "help", "add", "add-full", "change", "edit-contact", "edit-email", "edit-address",
    "phone", "show", "add-birthday", "show-birthday", "birthdays",
    "delete", "all", "add-note", "show-notes", "find-note", "edit-note", "delete-note"
]

notebook = load_notes()  # ✅ Ініціалізуємо нотатник

def suggest_command(user_input):
    suggestion = get_close_matches(user_input, ALL_COMMANDS, n=1)
    return suggestion[0] if suggestion else None

def execute_command(command, args):
    try:
        if command == "help":
            return """
I'm your new contact manager.
Available commands:
add [username] [phone] - Add a new contact
add-full [username] [phone] [email] [address] [DD.MM.YYYY] - Add a new contact with full details
change [username] [new_phone] - Change the phone number of a contact
edit-contact [username] [phone] [email] [address] [birthday] - Edit a contact's details
edit-email [username] [new_email] - Edit the email of a contact
edit-address [username] [new_address] - Edit the address of a contact
phone [username] - Show the phone number of a contact
show [username] - Show all details of a contact
add-birthday [username] [DD.MM.YYYY] - Add a birthday to a contact
show-birthday [username] - Show the birthday of a contact
birthdays - Show all contacts with birthdays
delete [username] - Delete a contact
all - Show all contacts
add-note [text] [tag1,tag2,...] - Add a note with tags
show-notes - Show all notes
find-note [keyword] - Find notes by keyword
edit-note [index] [new text] [new_tag1,new_tag2,...] - Edit a note by index
delete-note [index] - Delete a note by index
"""

        elif command == "add":
            if len(args) != 2:
                return "Invalid command. Use: add [username] [phone]"
            return add_contact(args[0], args[1])

        elif command == "add-full":
            if len(args) != 5:
                return "Invalid command. Use: add-full [username] [phone] [email] [address] [DD.MM.YYYY]"
            return add_full_contact(*args)

        elif command == "change":
            if len(args) != 2:
                return "Invalid command. Use: change [username] [new_phone]"
            return change_contact(args[0], args[1])

        elif command == "edit-contact":
            if len(args) < 2:
                return "Invalid command. Use: edit-contact [username] [phone] [email] [address] [birthday]"
            name = args[0]
            phone = args[1] if len(args) > 1 else None
            email = args[2] if len(args) > 2 else None
            address = args[3] if len(args) > 3 else None
            birthday = args[4] if len(args) > 4 else None
            return edit_contact(name, phone, email, address, birthday)

        elif command == "edit-email":
            if len(args) != 2:
                return "Invalid command. Use: edit-email [username] [new_email]"
            return edit_email(args[0], args[1])

        elif command == "edit-address":
            if len(args) != 2:
                return "Invalid command. Use: edit-address [username] [new_address]"
            return edit_address(args[0], args[1])

        elif command == "phone":
            if len(args) != 1:
                return "Invalid command. Use: phone [username]"
            return show_phone(args[0])

        elif command == "show":
            if len(args) != 1:
                return "Invalid command. Use: show [username]"
            return show_contact(args[0])

        elif command == "add-birthday":
            if len(args) != 2:
                return "Invalid command. Use: add-birthday [username] [DD.MM.YYYY]"
            return add_birthday(args[0], args[1])

        elif command == "show-birthday":
            if len(args) != 1:
                return "Invalid command. Use: show-birthday [username]"
            return show_birthday(args[0])

        elif command == "birthdays":
            return birthdays()

        elif command == "delete":
            if len(args) != 1:
                return "Invalid command. Use: delete [username]"
            return delete_contact(args[0])

        elif command == "all":
            return "\n".join(show_all())  # ✅ Виводимо всі контакти у вигляді рядків

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
        
        elif command == "all":
            return "\n".join(show_all())


        else:
            suggestion = suggest_command(command)
            if suggestion:
                return f"Unknown command '{command}'. Did you mean: '{suggestion}'?"
            return "Invalid command. Please try again."

    except Exception as e:
        return f"An error occurred: {e}"

