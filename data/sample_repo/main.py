"""Sample application for repository testing."""

from utils import format_message, add_numbers


def main():
    greeting = format_message("Hello")
    result = add_numbers(5, 7)

    print(greeting)
    print(f"5 + 7 = {result}")


if __name__ == "__main__":
    main()
