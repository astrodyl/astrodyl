import numpy as np


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
        if not isinstance(other, BoundedValue):
            return NotImplemented

        result = BoundedValue(self.value / other.value)
        result.lower = result.value * float(np.sqrt((self.lower / self.value) ** 2 + (other.lower / other.value) ** 2))
        result.upper = result.value * float(np.sqrt((self.upper / self.value) ** 2 + (other.upper / other.value) ** 2))
        return result

    def __mul__(self, other):
        """ Returns a BoundedValue with the value equal to the multiplication
        of the two values. The new bounds are calculated using quadrature.
        This method ignores any correlation between two values.

        :param other: BoundedValue
        :return: Resultant BoundedValue
        """
        if not isinstance(other, BoundedValue):
            return NotImplemented

        result = BoundedValue(self.value * other.value)
        result.lower = result.value * float(np.sqrt((self.lower / self.value) ** 2 + (other.lower / other.value) ** 2))
        result.upper = result.value * float(np.sqrt((self.upper / self.value) ** 2 + (other.upper / other.value) ** 2))
        return result
