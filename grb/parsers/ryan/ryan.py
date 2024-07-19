from grb.parsers.liao.entry import GRB
from grb.utils.io import txt
from grb.utils.math.bounded_value import BoundedValue


class Ryan:
    def __init__(self, path: str):
        self.grbs = None
        self.path = path
        self.parse(txt.read(path))

    def parse(self, lines: list, comment: str = '#') -> None:
        self.grbs = []

        for line in lines:
            if line.startswith(comment):
                continue

            line = line.split('\t')

            grb = GRB()
            grb.id = line[0]

            opening = line[1].replace('+', '').split(' ')
            grb.opening = BoundedValue(float(opening[0]), abs(float(opening[2])), float(opening[1]))

            ratio = line[2].replace('+', '').split(' ')
            grb.ratio = BoundedValue(float(ratio[0]), abs(float(ratio[2])), float(ratio[1]))

            grb.viewing = grb.ratio * grb.opening
            grb.off_axis_confidence = grb.viewing.value / grb.viewing.lower

            self.grbs.append(grb)

    def plot(self):
        pass


if __name__ == '__main__':
    input_path = r"C:\Projects\repos\grb\grb\resources\grbs_ryan_2015.txt"
    sources = Ryan(input_path)
    print()
