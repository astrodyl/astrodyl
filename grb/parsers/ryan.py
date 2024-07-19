from grb.definitions.bounded_value import BoundedValue
from grb.definitions.entry import GRB
from grb.utils.io import txt


"""
    ryan.py
    
    Parses data from Table 4 of Ryan et al. 2015. Each row of the table is
    parsed and stored in a GRB object defined in grb/definitions/entry.py.
    
    Ryan ran MCMC using the viewing angle / opening angle as a fitting parameter
    rather than the viewing angle on its own. The BoundedValue class is used to 
    easily transform this ratio to the viewing angle. Any correlations between the
    viewing angle and opening angle are ignored in the transformation.
    
    GAMMA RAY BURSTS ARE OBSERVED OFF-AXIS (2015):
        - https://arxiv.org/pdf/1405.5516
        
    Results from Ryan et al. 2015:
        - https://cosmo.nyu.edu/afterglowlibrary/
"""


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


if __name__ == '__main__':
    sources = Ryan(r"C:\Projects\repos\grb\grb\resources\grbs_ryan_2015.txt")

    print(len(sources.grbs))
