import sys
import os
from parser import parse_input
from commands import execute_command
from storage import contacts, save_data, set_data_directory

def main(directory=None):
    print("Welcome to the assistant bot!")
    
    if directory:
        if not os.path.exists(directory):
            os.makedirs(directory)
        set_data_directory(directory)

    while True:
        user_input = input("Enter a command please or"
        " 'help' for assistance: ").strip()
        if not user_input:
            continue

        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(contacts)
            break
        else:
            print(execute_command(command, args))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Використання: python main.py <шлях до директорії>")
        sys.exit(1)
        
    # Якщо аргумент командного рядка передано, використовуємо його
    directory_path = sys.argv[1] 

    # Передаємо шлях до функції main
    main(directory_path)

