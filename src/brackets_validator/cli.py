from .validator import UnbalancedBracketsError, highlight, validate


def main():
    text = input("Введіть строку: ")
    try:
        validate(text)
    except UnbalancedBracketsError as exc:
        print(text)
        print(highlight(text, exc.positions))
        raise
    print("Строка валідна")
