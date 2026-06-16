"""Calculation classes and factory for the calculator.

Defines the Calculation abstract base class, the CalculationFactory that
builds calculation instances by name, and the four concrete operation classes.
"""

from abc import ABC, abstractmethod
from app.operation import Operation


class Calculation(ABC):
    """Abstract base class for all calculations.

    Each calculation stores two operands and must implement execute() to
    produce a result, giving every calculation type a consistent interface.
    """

    symbol: str = ""

    def __init__(self, a: float, b: float) -> None:
        """Store the two operands.

        Args:
            a: The first operand.
            b: The second operand.
        """
        self.a = a
        self.b = b

    @abstractmethod
    def execute(self) -> float:
        """Perform the calculation and return its result.

        Subclasses must implement this method.
        """
        pass  # pragma: no cover

    @staticmethod
    def _format(value: float):
        """Show whole numbers without a trailing '.0' and keep real decimals."""
        return int(value) if value == int(value) else value

    def __str__(self) -> str:
        """Return a readable summary in the form '<a> <symbol> <b> = <result>'."""
        result = self.execute()
        return f"{self._format(self.a)} {self.symbol} {self._format(self.b)} = {self._format(result)}"

    def __repr__(self) -> str:
        """Return an unambiguous representation in the form '<Class>(a=..., b=...)'."""
        return f"{self.__class__.__name__}(a={self.a}, b={self.b})"


class CalculationFactory:
    """Registry-based factory that creates Calculation instances by name."""

    _calculations = {}

    @classmethod
    def register_calculation(cls, calculation_type: str):
        """Return a class decorator that registers a Calculation subclass.

        Args:
            calculation_type: The name to register the subclass under.

        Returns:
            A decorator that records the subclass in the registry.

        Raises:
            ValueError: If the name is already registered.
        """
        def decorator(subclass):
            key = calculation_type.lower()
            if key in cls._calculations:
                raise ValueError(f"Calculation type '{calculation_type}' is already registered.")
            cls._calculations[key] = subclass
            return subclass
        return decorator

    @classmethod
    def create_calculation(cls, calculation_type: str, a: float, b: float) -> Calculation:
        """Create a Calculation for the given type.

        Args:
            calculation_type: The registered name of the calculation.
            a: The first operand.
            b: The second operand.

        Returns:
            An instance of the matching Calculation subclass.

        Raises:
            ValueError: If the type is not registered.
        """
        key = calculation_type.lower()
        calculation_class = cls._calculations.get(key)
        if not calculation_class:
            available = ", ".join(cls._calculations.keys())
            raise ValueError(f"Unsupported calculation type: '{calculation_type}'. Available types: {available}")
        return calculation_class(a, b)


@CalculationFactory.register_calculation("add")
class AdditionCalculation(Calculation):
    """Addition of two numbers."""

    symbol = "+"

    def execute(self) -> float:
        """Return the sum of the two operands."""
        return Operation.addition(self.a, self.b)


@CalculationFactory.register_calculation("subtract")
class SubtractionCalculation(Calculation):
    """Subtraction of two numbers."""

    symbol = "-"

    def execute(self) -> float:
        """Return the difference of the two operands."""
        return Operation.subtraction(self.a, self.b)


@CalculationFactory.register_calculation("multiply")
class MultiplicationCalculation(Calculation):
    """Multiplication of two numbers."""

    symbol = "*"

    def execute(self) -> float:
        """Return the product of the two operands."""
        return Operation.multiplication(self.a, self.b)


@CalculationFactory.register_calculation("divide")
class DivisionCalculation(Calculation):
    """Division of two numbers."""

    symbol = "/"

    def execute(self) -> float:
        """Return the quotient of the two operands.

        Raises:
            ZeroDivisionError: If the divisor is zero.
        """
        if self.b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return Operation.division(self.a, self.b)