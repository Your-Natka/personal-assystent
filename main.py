from colorama import init, Fore, Style
import sys
import os
from parser import parse_input
from commands import execute_command
from storage import contacts, save_data, set_data_directory
from difflib import get_close_matches

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
        "birthdays-in   - show birthdays in given days\n"
        "help           - show this help message\n"
        "back           - return to main menu" +
        Style.RESET_ALL
    )

def notes_help():
    print(Fore.MAGENTA + "Available commands:" + Style.RESET_ALL)
    print(
    Fore.GREEN +
        "add-note         - add a note with tags\n"
        "show-notes       - show all notes\n"
        "sort-notes       - sort notes by first tag\n"
        "find-note        - find notes by keyword\n"
        "edit-note        - edit note by index\n"
        "delete-note      - delete note by index\n"
        "help             - show this help message\n"
        "back             - return to main menu" +
        Style.RESET_ALL
    )
def suggest_command(user_input, allowed_commands):
    matches = get_close_matches(user_input, allowed_commands, n=1, cutoff=0.5)
    return matches[0] if matches else None

def main(directory=None):
    print(Fore.BLUE + "Welcome to the assistant bot!" + Style.RESET_ALL)

    if directory:
        if not os.path.exists(directory):
            os.makedirs(directory)
        set_data_directory(directory)

    while True:
        try:
            user_input = input(f"{Fore.YELLOW}Enter mode (contacts/notes or exit/close): {Style.RESET_ALL}").strip().lower()
            if user_input == '':
                mode = 'contacts'  # дефолтний режим
            else:
                mode = user_input

            if mode in ['exit', 'close']:
                print(Fore.CYAN + "Good bye!" + Style.RESET_ALL)
                save_data(contacts)
                break

            if mode not in ['contacts', 'notes']:
                print("Unknown mode. Please enter 'contacts', 'notes', or 'exit'.")
                continue

            print(f"Entering {mode} mode (type '{Fore.LIGHTRED_EX}help{Style.RESET_ALL}' for available commands)")

            while True:
                user_input = input(f"{Fore.YELLOW}Enter command:{Style.RESET_ALL} ").strip()
                if not user_input:
                    print("Returning to mode selection...")
                    break

                command, args = parse_input(user_input)
                command = command.lower()

                if command == 'hello':
                    print("How can I help you?")
                    continue

                if command == 'back':
                    print("Returning to mode selection...")
                    break

                if command in ['exit', 'close']:
                    print(Fore.CYAN + "Good bye!" + Style.RESET_ALL)
                    save_data(contacts)
                    return

                if mode == 'contacts':
                    allowed_commands = ['add', 'edit', 'delete', 'search', 'all', 'birthdays-in', 'hello', 'help']
                else:
                    allowed_commands = ['add-note', 'show-notes', 'sort-notes', 'find-note', 'edit-note', 'delete-note', 'hello', 'help']

                if command in allowed_commands:
                    if command == 'help':
                        if mode == 'contacts':
                            contacts_help()
                        else:
                            notes_help()
                    else:
                        print(execute_command(command, args))
                else:
                    suggestion = suggest_command(command, allowed_commands)
                    if suggestion:
                        answer = input(
                            f"{Fore.CYAN}Unknown command '{command}'. Did you mean '{Fore.GREEN}{suggestion}{Fore.CYAN}'? (y/n): {Style.RESET_ALL}"
                        ).strip().lower()
                        if answer == 'y':
                            print(execute_command(suggestion, args))
                        else:
                            print(Fore.RED + "Command not recognized. Type 'help' to see available commands." + Style.RESET_ALL)
                    else:
                        print(Fore.RED + "Command not recognized. Type 'help' to see available commands." + Style.RESET_ALL)

        except KeyboardInterrupt:
            print("\nInterrupted by user. Exiting...")
            save_data(contacts)
            break


if __name__ == "__main__":
    if len(sys.argv) == 2:
        directory_path = sys.argv[1]
    else:
        directory_path = '.'  # поточна директорія
    main(directory_path)
    