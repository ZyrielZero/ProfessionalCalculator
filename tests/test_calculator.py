import pytest
from io import StringIO
from app.calculator import display_help, display_history, calculator
from app.calculation import CalculationFactory


def feed_input(monkeypatch, text):
    monkeypatch.setattr("sys.stdin", StringIO(text))


# ----- display_help -----

def test_display_help(capsys):
    display_help()
    captured = capsys.readouterr()
    assert "Calculator REPL Help" in captured.out
    assert "Supported operations" in captured.out


# ----- display_history -----

def test_display_history_empty(capsys):
    display_history([])
    captured = capsys.readouterr()
    assert captured.out.strip() == "No calculations performed yet."

def test_display_history_with_entries(capsys):
    calc = CalculationFactory.create_calculation("add", 8.0, 3.0)
    display_history([calc])
    captured = capsys.readouterr()
    assert "Calculation History:" in captured.out
    assert "1. AdditionCalculation: 8.0 Addition 3.0 = 11.0" in captured.out


# ----- Special commands -----

def test_calculator_exit(monkeypatch, capsys):
    feed_input(monkeypatch, "exit\n")
    with pytest.raises(SystemExit) as exc_info:
        calculator()
    captured = capsys.readouterr()
    assert "Exiting calculator. Goodbye!" in captured.out
    assert exc_info.value.code == 0

def test_calculator_help_command(monkeypatch, capsys):
    feed_input(monkeypatch, "help\nexit\n")
    with pytest.raises(SystemExit):
        calculator()
    captured = capsys.readouterr()
    assert "Calculator REPL Help" in captured.out

def test_calculator_history_command(monkeypatch, capsys):
    feed_input(monkeypatch, "add 8 3\nhistory\nexit\n")
    with pytest.raises(SystemExit):
        calculator()
    captured = capsys.readouterr()
    assert "Result: AdditionCalculation: 8.0 Addition 3.0 = 11.0" in captured.out
    assert "Calculation History:" in captured.out
    assert "1. AdditionCalculation: 8.0 Addition 3.0 = 11.0" in captured.out


# ----- Operations -----

@pytest.mark.parametrize("command, expected", [
    ("add 8 3", "Result: AdditionCalculation: 8.0 Addition 3.0 = 11.0"),
    ("subtract 8 3", "Result: SubtractionCalculation: 8.0 Subtraction 3.0 = 5.0"),
    ("multiply 8 3", "Result: MultiplicationCalculation: 8.0 Multiplication 3.0 = 24.0"),
    ("divide 8 2", "Result: DivisionCalculation: 8.0 Division 2.0 = 4.0"),
])
def test_calculator_operations(monkeypatch, capsys, command, expected):
    feed_input(monkeypatch, f"{command}\nexit\n")
    with pytest.raises(SystemExit):
        calculator()
    captured = capsys.readouterr()
    assert expected in captured.out


# ----- Error handling -----

def test_calculator_invalid_format(monkeypatch, capsys):
    feed_input(monkeypatch, "add 5\nexit\n")
    with pytest.raises(SystemExit):
        calculator()
    captured = capsys.readouterr()
    assert "Invalid input. Please follow the format:" in captured.out

def test_calculator_invalid_numbers(monkeypatch, capsys):
    feed_input(monkeypatch, "add x y\nexit\n")
    with pytest.raises(SystemExit):
        calculator()
    captured = capsys.readouterr()
    assert "Invalid input. Please follow the format:" in captured.out

def test_calculator_unsupported_operation(monkeypatch, capsys):
    feed_input(monkeypatch, "modulus 2 3\nexit\n")
    with pytest.raises(SystemExit):
        calculator()
    captured = capsys.readouterr()
    assert "Unsupported calculation type: 'modulus'." in captured.out
    assert "Type 'help' to see the list of supported operations." in captured.out

def test_calculator_division_by_zero(monkeypatch, capsys):
    feed_input(monkeypatch, "divide 8 0\nexit\n")
    with pytest.raises(SystemExit):
        calculator()
    captured = capsys.readouterr()
    assert "Cannot divide by zero." in captured.out


# ----- Graceful interrupts -----

def test_calculator_keyboard_interrupt(monkeypatch, capsys):
    def raise_keyboard_interrupt(prompt):
        raise KeyboardInterrupt
    monkeypatch.setattr("builtins.input", raise_keyboard_interrupt)
    with pytest.raises(SystemExit) as exc_info:
        calculator()
    captured = capsys.readouterr()
    assert "Keyboard interrupt detected." in captured.out
    assert exc_info.value.code == 0

def test_calculator_eof(monkeypatch, capsys):
    def raise_eof(prompt):
        raise EOFError
    monkeypatch.setattr("builtins.input", raise_eof)
    with pytest.raises(SystemExit) as exc_info:
        calculator()
    captured = capsys.readouterr()
    assert "EOF detected." in captured.out
    assert exc_info.value.code == 0


# ----- Unexpected error during execution -----

def test_calculator_unexpected_exception(monkeypatch, capsys):
    class MockCalculation:
        def execute(self):
            raise Exception("unexpected failure")

    def mock_create(operation, a, b):
        return MockCalculation()

    monkeypatch.setattr(CalculationFactory, "create_calculation", mock_create)
    feed_input(monkeypatch, "add 8 3\nexit\n")
    with pytest.raises(SystemExit):
        calculator()
    captured = capsys.readouterr()
    assert "An error occurred during calculation: unexpected failure" in captured.out
    assert "Please try again." in captured.out