from cm.definitions.hardware.filter import Filter
from cm.definitions.hardware.telescope import Telescope


class Hardware:
    def __init__(self, filter_: Filter, telescope: Telescope):
        self.filter = filter_
        self.telescope = telescope
