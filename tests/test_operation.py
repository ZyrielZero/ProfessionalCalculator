import pytest
from app.operation import Operation


# ----- Addition -----

def test_addition_positive():
    a = 1.0
    b = 2.0
    expected_result = 3.0
    result = Operation.addition(a, b)
    assert result == expected_result, f"Expected {a} + {b} to be {expected_result}, but got {result}"

def test_addition_negative():
    a = -4.0
    b = -6.0
    expected_result = -10.0
    result = Operation.addition(a, b)
    assert result == expected_result, f"Expected {a} + {b} to be {expected_result}, but got {result}"

def test_addition_mixed():
    a = 7.0
    b = -2.0
    expected_result = 5.0
    result = Operation.addition(a, b)
    assert result == expected_result, f"Expected {a} + {b} to be {expected_result}, but got {result}"

def test_addition_with_zero():
    a = 9.0
    b = 0.0
    expected_result = 9.0
    result = Operation.addition(a, b)
    assert result == expected_result, f"Expected {a} + {b} to be {expected_result}, but got {result}"


# ----- Subtraction -----

def test_subtraction_positive():
    a = 2.0
    b = 1.0
    expected_result = 1.0
    result = Operation.subtraction(a, b)
    assert result == expected_result, f"Expected {a} - {b} to be {expected_result}, but got {result}"

def test_subtraction_negative():
    a = -5.0
    b = -3.0
    expected_result = -2.0
    result = Operation.subtraction(a, b)
    assert result == expected_result, f"Expected {a} - {b} to be {expected_result}, but got {result}"

def test_subtraction_mixed():
    a = 8.0
    b = -2.0
    expected_result = 10.0
    result = Operation.subtraction(a, b)
    assert result == expected_result, f"Expected {a} - {b} to be {expected_result}, but got {result}"

def test_subtraction_with_zero():
    a = 6.0
    b = 0.0
    expected_result = 6.0
    result = Operation.subtraction(a, b)
    assert result == expected_result, f"Expected {a} - {b} to be {expected_result}, but got {result}"


# ----- Multiplication -----

def test_multiplication_positive():
    a = 2.0
    b = 3.0
    expected_result = 6.0
    result = Operation.multiplication(a, b)
    assert result == expected_result, f"Expected {a} * {b} to be {expected_result}, but got {result}"

def test_multiplication_negative():
    a = -3.0
    b = -4.0
    expected_result = 12.0
    result = Operation.multiplication(a, b)
    assert result == expected_result, f"Expected {a} * {b} to be {expected_result}, but got {result}"

def test_multiplication_mixed():
    a = 5.0
    b = -2.0
    expected_result = -10.0
    result = Operation.multiplication(a, b)
    assert result == expected_result, f"Expected {a} * {b} to be {expected_result}, but got {result}"

def test_multiplication_with_zero():
    a = 7.0
    b = 0.0
    expected_result = 0.0
    result = Operation.multiplication(a, b)
    assert result == expected_result, f"Expected {a} * {b} to be {expected_result}, but got {result}"


# ----- Division -----

def test_division_positive():
    a = 6.0
    b = 3.0
    expected_result = 2.0
    result = Operation.division(a, b)
    assert result == expected_result, f"Expected {a} / {b} to be {expected_result}, but got {result}"

def test_division_negative():
    a = -8.0
    b = -2.0
    expected_result = 4.0
    result = Operation.division(a, b)
    assert result == expected_result, f"Expected {a} / {b} to be {expected_result}, but got {result}"

def test_division_mixed():
    a = 9.0
    b = -3.0
    expected_result = -3.0
    result = Operation.division(a, b)
    assert result == expected_result, f"Expected {a} / {b} to be {expected_result}, but got {result}"

def test_division_zero_numerator():
    a = 0.0
    b = 5.0
    expected_result = 0.0
    result = Operation.division(a, b)
    assert result == expected_result, f"Expected {a} / {b} to be {expected_result}, but got {result}"

def test_division_by_zero():
    a = 6.0
    b = 0.0
    with pytest.raises(ValueError) as exc_info:
        Operation.division(a, b)
    assert str(exc_info.value) == "Error: Cannot divide by zero.", f"Expected ValueError with message 'Error: Cannot divide by zero.', but got '{str(exc_info.value)}'"


# ----- Negative tests: invalid input types -----

@pytest.mark.parametrize("method, a, b, expected_exception", [
    (Operation.addition, "1", 2.0, TypeError),
    (Operation.subtraction, 2.0, "1", TypeError),
    (Operation.multiplication, "2", "3", TypeError),
    (Operation.division, 6.0, "3", TypeError),
])
def test_operations_invalid_input_types(method, a, b, expected_exception):
    with pytest.raises(expected_exception):
        method(a, b)