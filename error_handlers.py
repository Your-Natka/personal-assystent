def input_error(func):
    """
    Декоратор для обробки помилок введення.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            return f"Error: {str(e)}"
        except ValueError as e:
            return f"Invalid input: {str(e)}"
        except IndexError as e:
            return f"Index error: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    return wrapper