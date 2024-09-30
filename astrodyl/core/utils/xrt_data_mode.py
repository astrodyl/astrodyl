

"""
    XRTDataMode class

    Swift's XRT has multiple data modes (e.g., photon counting,
    windowed timing) each of which contain the same type of data.
"""


class XRTDataMode:
    def __init__(self):
        self.times: list = []
        self.time_lowers: list = []
        self.time_uppers: list = []

        self.fluxes: list = []
        self.flux_lowers: list = []
        self.flux_uppers: list = []