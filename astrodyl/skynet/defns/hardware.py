from astrodyl.skynet.defns.filter import Filter
from astrodyl.skynet.defns.telescope import Telescope


class Hardware:
    def __init__(self, filter_: Filter, telescope: Telescope):
        self.filter = filter_
        self.telescope = telescope
