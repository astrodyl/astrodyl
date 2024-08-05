

class Filter:
    def __init__(self, name: str, frequency: float, efficiency: float, zero_point: float):
        self.name = name
        self.frequency = frequency
        self.efficiency = efficiency
        self.zero_point = zero_point

    def wavelength(self, um: bool = False) -> float:
        """ Returns the wavelength of the filter.

        :param um: returns wavelength in units of micro-meters if True
        """
        return 2.998e8 / self.frequency * (10e5 if um else 1.0)