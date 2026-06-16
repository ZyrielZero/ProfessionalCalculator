import pytest
from unittest.mock import patch
from app.operation import Operation
from app.calculation import (
    CalculationFactory,
    Calculation,
    AdditionCalculation,
    SubtractionCalculation,
    MultiplicationCalculation,
    DivisionCalculation,
)


# ----- execute() delegates to Operation (mocked for isolation) -----

@patch.object(Operation, "addition")
def test_addition_execute_calls_operation(mock_addition):
    mock_addition.return_value = 11.0
    calc = AdditionCalculation(8.0, 3.0)
    result = calc.execute()
    mock_addition.assert_called_once_with(8.0, 3.0)
    assert result == 11.0

@patch.object(Operation, "subtraction")
def test_subtraction_execute_calls_operation(mock_subtraction):
    mock_subtraction.return_value = 5.0
    calc = SubtractionCalculation(8.0, 3.0)
    result = calc.execute()
    mock_subtraction.assert_called_once_with(8.0, 3.0)
    assert result == 5.0

@patch.object(Operation, "multiplication")
def test_multiplication_execute_calls_operation(mock_multiplication):
    mock_multiplication.return_value = 24.0
    calc = MultiplicationCalculation(8.0, 3.0)
    result = calc.execute()
    mock_multiplication.assert_called_once_with(8.0, 3.0)
    assert result == 24.0

@patch.object(Operation, "division")
def test_division_execute_calls_operation(mock_division):
    mock_division.return_value = 4.0
    calc = DivisionCalculation(8.0, 2.0)
    result = calc.execute()
    mock_division.assert_called_once_with(8.0, 2.0)
    assert result == 4.0


# ----- execute() propagates an error raised by Operation (negative) -----

@patch.object(Operation, "addition", side_effect=ValueError("operation failed"))
def test_addition_execute_propagates_error(mock_addition):
    calc = AdditionCalculation(8.0, 3.0)
    with pytest.raises(ValueError) as exc_info:
        calc.execute()
    assert str(exc_info.value) == "operation failed"


# ----- Factory creates the correct subclass -----

@pytest.mark.parametrize("calc_type, expected_cls", [
    ("add", AdditionCalculation),
    ("subtract", SubtractionCalculation),
    ("multiply", MultiplicationCalculation),
    ("divide", DivisionCalculation),
])
def test_factory_creates_correct_type(calc_type, expected_cls):
    calc = CalculationFactory.create_calculation(calc_type, 8.0, 3.0)
    assert isinstance(calc, expected_cls)
    assert calc.a == 8.0
    assert calc.b == 3.0


def test_factory_unsupported_type_raises():
    with pytest.raises(ValueError) as exc_info:
        CalculationFactory.create_calculation("modulus", 8.0, 3.0)
    assert "Unsupported calculation type: 'modulus'." in str(exc_info.value)


def test_factory_duplicate_registration_raises():
    with pytest.raises(ValueError) as exc_info:
        @CalculationFactory.register_calculation("add")
        class AnotherAddition(Calculation):
            def execute(self) -> float:
                return Operation.addition(self.a, self.b)
    assert "Calculation type 'add' is already registered." in str(exc_info.value)


# ----- Divide by zero (real guard, not mocked) -----

def test_division_by_zero_raises():
    calc = DivisionCalculation(8.0, 0.0)
    with pytest.raises(ZeroDivisionError) as exc_info:
        calc.execute()
    assert str(exc_info.value) == "Cannot divide by zero."


# ----- String representation -----

@pytest.mark.parametrize("calc_type, a, b, mock_attr, mock_value, expected", [
    ("add", 8.0, 3.0, "addition", 11.0, "8 + 3 = 11"),
    ("subtract", 8.0, 3.0, "subtraction", 5.0, "8 - 3 = 5"),
    ("multiply", 8.0, 3.0, "multiplication", 24.0, "8 * 3 = 24"),
    ("divide", 7.0, 2.0, "division", 3.5, "7 / 2 = 3.5"),
])
def test_str_representation(calc_type, a, b, mock_attr, mock_value, expected):
    with patch.object(Operation, mock_attr, return_value=mock_value):
        calc = CalculationFactory.create_calculation(calc_type, a, b)
        assert str(calc) == expected


def test_repr_representation():
    calc = SubtractionCalculation(8.0, 3.0)
    assert repr(calc) == "SubtractionCalculation(a=8.0, b=3.0)"