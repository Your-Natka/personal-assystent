import sys
from parser import parse_input
from commands import execute_command
from storage import contacts, save_data

def main(directory=None):
    print("Welcome to the assistant bot!")
   
    while True:
        user_input = input("Enter a command: ").strip()
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
    directory_path = sys.argv[1] if len(sys.argv) > 1 else None

    # Передаємо шлях до функції main
    main(directory_path)

