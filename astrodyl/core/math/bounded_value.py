import numpy as np
import operator


class BoundedValue:
    def __init__(self, value: float = None, lower: float = None, upper: float = None):
        self.value = value
        self.lower = lower
        self.upper = upper

    def __truediv__(self, other):
        """ Returns a BoundedValue with the value equal to the division
        of the two values. The new bounds are calculated using quadrature.

        :param other: BoundedValue
        :return: Resultant BoundedValue
        """
        return self.perform_operation(other, operator.__truediv__)

    def __mul__(self, other):
        """ Returns a BoundedValue with the value equal to the multiplication
        of the two values. The new bounds are calculated using quadrature.
        This method ignores any correlation between two values.

        :param other: BoundedValue
        :return: Resultant BoundedValue
        """
        return self.perform_operation(other, operator.__mul__)

    def perform_operation(self, other, operation):
        """ Performs the operation on the BoundedValues. Performs error
        propagation assuming that the two values are not correlated.

        Supported operations:
            - multiplication
            - division

        :param other: BoundedValue
        :param operation: Operator.__mul__ or Operator.__truediv__
        :return: Resultant BoundedValue
        """
        if not isinstance(other, BoundedValue):
            return NotImplemented

        result = BoundedValue()

        if operation == operator.__truediv__:
            result.value = self.value / other.value
        elif operation == operator.__mul__:
            result.value = self.value * other.value
        else:
            return NotImplemented

        result.lower = result.value * float(np.sqrt((self.lower / self.value) ** 2 + (other.lower / other.value) ** 2))
        result.upper = result.value * float(np.sqrt((self.upper / self.value) ** 2 + (other.upper / other.value) ** 2))

        return result
