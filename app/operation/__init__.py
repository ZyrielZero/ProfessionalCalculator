"""Arithmetic operations for the calculator.

Defines the Operation class, which exposes the four basic arithmetic
operations as stateless static methods.
"""


class Operation:
    """Groups the four basic arithmetic operations as static methods.

    The methods are static because they depend only on their arguments and
    hold no per-instance state, so the class never needs to be instantiated.
    """

    @staticmethod
    def addition(a: float, b: float) -> float:
        """Return the sum of two numbers.

        Args:
            a: The first operand.
            b: The second operand.

        Returns:
            The sum of a and b.
        """
        return a + b

    @staticmethod
    def subtraction(a: float, b: float) -> float:
        """Return the difference of two numbers.

        Args:
            a: The number to subtract from.
            b: The number to subtract.

        Returns:
            The result of a minus b.
        """
        return a - b

    @staticmethod
    def multiplication(a: float, b: float) -> float:
        """Return the product of two numbers.

        Args:
            a: The first operand.
            b: The second operand.

        Returns:
            The product of a and b.
        """
        return a * b

    @staticmethod
    def division(a: float, b: float) -> float:
        """Return the quotient of two numbers.

        Args:
            a: The dividend.
            b: The divisor.

        Returns:
            The result of a divided by b.

        Raises:
            ValueError: If b is zero.
        """
        if b == 0:
            raise ValueError("Error: Cannot divide by zero.")
        return a / b