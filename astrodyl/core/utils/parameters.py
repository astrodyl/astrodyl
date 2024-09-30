from astrodyl.skynet.defns.filter import Filter


class Parameters:
    def __init__(self, filter_: Filter, time: float, magnitude: float):
        """
        :param filter_: filter used in the image
        :param time: time in seconds since the trigger time
        :param magnitude: magnitude of the transient in the image
        """
        self.filter: Filter = filter_
        self.time: float = time
        self.magnitude: float = magnitude
