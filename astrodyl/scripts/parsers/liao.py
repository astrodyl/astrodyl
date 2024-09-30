from astrodyl.core.utils.entry import GRB
from astrodyl.core.io import txt

"""
    liao.py
    
    Parses Table 2 of Liao et al 2024 as well as the table found in the 
    supplement section. Each row of the table is parsed and stored in a
    GRB object defined in grb/definitions/entry.py.
    
    A comparative study of outflow structures of two classes of gamma-ray
    bursts (2024):
        - https://doi.org/10.1093/mnras/stae1043
"""


class Liao:
    def __init__(self, path: str):
        self.grbs = None
        self.path = path
        self.parse(txt.read(path))

    def parse(self, lines: list, comment: str = '#') -> None:
        """ Parses the Gamma-Ray Burst tables.

        :param lines: list of grb data strings
        :param comment: character for comments
        """
        self.grbs = []

        for line in lines:
            if line.startswith(comment):
                continue

            self.grbs.append(GRB(line.split('\t')))


if __name__ == '__main__':
    sources = Liao(r"/grb/resources/grbs_laio_2024.txt")

    print(len(sources.grbs))
