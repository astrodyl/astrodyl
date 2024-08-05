

class Transient:
    def __init__(self, trigger_time: float, a: float, b: float, ebv: float):
        """
        :param trigger_time:
        :param a: temporal index (typically denoted by alpha)
        :param b: spectral index (typically denoted by beta)
        :param ebv: dust extinction E(B - V)
        """
        self.trigger_time = trigger_time
        self.temporal_index = a
        self.spectral_index = b
        self.ebv = ebv

