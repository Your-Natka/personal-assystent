def parse_input(user_input):
    """
    Розбирає введений рядок на команду та аргументи.
    Працює з командами, де імена або дані можуть містити пробіли.
    """
    parts = user_input.strip().split()
    if not parts:
        return "", []

    command = parts[0].lower()
    args = user_input[len(command):].strip().split(" ", maxsplit=2)

    return command, args
