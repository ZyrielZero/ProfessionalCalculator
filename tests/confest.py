import pytest

from app.calculation import (
    CalculationFactory,
    AdditionCalculation,
    SubtractionCalculation,
    MultiplicationCalculation,
    DivisionCalculation,
)

@pytest.fixture(autouse=True)
def reset_calculation_factory():
    CalculationFactory._calculations.clear()
    CalculationFactory.register_calculation("add")(AdditionCalculation)
    CalculationFactory.register_calculation("subtract")(SubtractionCalculation)
    CalculationFactory.register_calculation("multiply")(MultiplicationCalculation)
    CalculationFactory.register_calculation("divide")(DivisionCalculation)