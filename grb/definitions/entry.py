from grb.definitions.bounded_value import BoundedValue


class GRB:
    def __init__(self, line: str = None):
        self.id = None
        self.viewing = BoundedValue()
        self.opening = BoundedValue()
        self.ratio = BoundedValue()
        self.off_axis_confidence = None

        if line:
            self.parse(line)

    def parse(self, line: str):
        """ Parses a line from the grb_list_liao.txt file.
        """
        viewing = line[3].replace('+', '').split(' ')
        opening = line[4].replace('+', '').split(' ')

        self.id = line[0]
        self.viewing = BoundedValue(float(viewing[0]), abs(float(viewing[2])), float(viewing[1]))
        self.opening = BoundedValue(float(opening[0]), abs(float(opening[2])), float(opening[1]))
        self.ratio = self.viewing / self.opening
        self.off_axis_confidence = float(line[5])
