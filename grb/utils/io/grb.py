from typing import List


"""
    GRB.py
"""


def parse(lines: List[str], comment: str = '#') -> List[dict]:
    """ Parses the Gamma-Ray Burst tables.

    :param path: path to file
    :param comment: character for comments
    :return: parsed data as a list of dictionaries
    """
    data = []

    for line in lines:
        if line.startswith(comment):
            continue

        grb, line = {}, line.split('\t')

        viewing_angle = line[3].replace('+', '').split(' ')
        opening_angle = line[4].replace('+', '').split(' ')

        data.append({
            'GRB': line[0],
            'viewing': float(viewing_angle[0]),
            'viewing_upper': float(viewing_angle[1]),
            'viewing_lower': abs(float(viewing_angle[2])),
            'viewing_confidence': float(line[5]),
            'opening': float(opening_angle[0]),
            'opening_upper': float(opening_angle[1]),
            'opening_lower': abs(float(opening_angle[2])),
            'angle_ratio': round(float(viewing_angle[0]) / float(opening_angle[0]), 2),
        })

    return data
