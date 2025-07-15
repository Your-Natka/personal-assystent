import shlex

def parse_input(user_input):
    """
    Розбирає введений рядок на команду та аргументи, враховуючи лапки.
    """
    parts = shlex.split(user_input)
    if not parts:
        return "", []

    command = parts[0].lower()
    args = parts[1:]
    return command, args
