"""Interactive REPL for the calculator.

Provides the read-eval-print loop along with help and history display, and
demonstrates both the LBYL (Look Before You Leap) and EAFP (Easier to Ask
Forgiveness than Permission) error-handling styles.
"""

import sys
from typing import List
from app.calculation import Calculation, CalculationFactory


def display_help() -> None:
    """Print usage instructions and the supported operations and commands."""
    help_message = """
Calculator REPL Help
--------------------
Usage:
    <operation> <number1> <number2>
    - Perform a calculation with the specified operation and two numbers.
    - Supported operations:
        add       : Adds two numbers.
        subtract  : Subtracts the second number from the first.
        multiply  : Multiplies two numbers.
        divide    : Divides the first number by the second.

Special Commands:
    help      : Display this help message.
    history   : Show the history of calculations.
    exit      : Exit the calculator.

Examples:
    add 10 5
    subtract 15.5 3.2
    multiply 7 8
    divide 20 4
"""
    print(help_message)


def display_history(history: List[Calculation]) -> None:
    """Print the calculations performed this session.

    Args:
        history: The list of completed calculations, in order.
    """
    if not history:
        print("No calculations performed yet.")
    else:
        print("Calculation History:")
        for index, calculation in enumerate(history, start=1):
            print(f"{index}. {calculation}")


def calculator() -> None:
    """Run the read-eval-print loop until the user exits.

    Each turn reads an operation and two numbers, builds the matching
    calculation through the factory, prints the result, and records it in the
    session history. Invalid input, unknown operations, division by zero, and
    keyboard/EOF interrupts are all handled gracefully.
    """
    history: List[Calculation] = []

    print("Welcome to the Professional Calculator REPL!")
    print("Type 'help' for instructions or 'exit' to quit.\n")

    while True:
        try:
            user_input = input(">> ").strip()

            # LBYL: check for empty input before doing any work.
            if not user_input:
                continue  # pragma: no cover

            command = user_input.lower()

            if command == "help":
                display_help()
                continue
            elif command == "history":
                display_history(history)
                continue
            elif command == "exit":
                print("Exiting calculator. Goodbye!\n")
                sys.exit(0)

            # EAFP: try to parse the input and catch failure instead of pre-validating.
            try:
                operation, num1_str, num2_str = user_input.split()
                num1 = float(num1_str)
                num2 = float(num2_str)
            except ValueError:
                print("Invalid input. Please follow the format: <operation> <num1> <num2>")
                print("Type 'help' for more information.\n")
                continue

            try:
                calculation = CalculationFactory.create_calculation(operation, num1, num2)
            except ValueError as error:
                print(error)
                print("Type 'help' to see the list of supported operations.\n")
                continue

            try:
                calculation.execute()
            except ZeroDivisionError:
                print("Cannot divide by zero.")
                print("Please enter a non-zero divisor.\n")
                continue
            except Exception as error:
                print(f"An error occurred during calculation: {error}")
                print("Please try again.\n")
                continue

            print(f"Result: {calculation}\n")
            history.append(calculation)

        except KeyboardInterrupt:
            print("\nKeyboard interrupt detected. Exiting calculator. Goodbye!")
            sys.exit(0)
        except EOFError:
            print("\nEOF detected. Exiting calculator. Goodbye!")
            sys.exit(0)


if __name__ == "__main__":
    calculator()  # pragma: no cover