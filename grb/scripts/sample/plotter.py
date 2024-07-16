import matplotlib.pyplot as plt
from typing import List

import mplcursors

from grb.utils.io import txt
from grb.utils.io import grb as parser

"""
    Plotter.py
    
    The Plotter plots the viewing angle confidence vs. viewing angle.
    This is useful for viewing which inferred viewing angles are high
    confidence. 
    
    This is a pretty specific script and should be considered more of a 
    sandbox tool than a generic plotting tool. If I create a generic 
    plotting tool, then I'll move this to a sandbox directory.
"""


def plot_viewing_angles(grbs: List[dict]) -> None:
    """ Plots the viewing angle confidence vs. viewing angle.

    Confidence Levels:
        - High: sigma >= 5
        - Mild: 3 <= sigma < 5
        - Low: sigma < 3
    """
    viewing, lower, labels_low = [], [], []
    viewing_3, lower_3, labels_3 = [], [], []
    viewing_5, lower_5, labels_5 = [], [], []

    for i, grb in enumerate(grbs):
        label = grb['GRB'] + '(' + str(grb['viewing']) + ',' + str(grb['viewing_lower']) + ')'

        if grb['viewing_confidence'] >= 5.0:
            labels_5.append(label)
            viewing_5.append(grb['viewing'])
            lower_5.append(grb['viewing_lower'])
        elif grb['viewing_confidence'] >= 3.0:
            labels_3.append(label)
            viewing_3.append(grb['viewing'])
            lower_3.append(grb['viewing_lower'])
        else:
            labels_low.append(label)
            viewing.append(grb['viewing'])
            lower.append(grb['viewing_lower'])

    fig, ax = plt.subplots()

    # Plot High Confidence Angles
    high = ax.scatter(viewing_5, lower_5, color='green', label='High Confidence')

    # Plot Mild Confidence Angles
    mild = ax.scatter(viewing_3, lower_3, color='purple', label='Mild Confidence')

    # Plot Low Confidence Angles
    low = ax.scatter(viewing, lower, color='black', label='Low Confidence')

    ax.legend()
    ax.set_ylabel("Lower Bound")
    ax.set_xlabel("Viewing Angle (rads)")
    ax.set_title("Lower Viewing Angle Bounds vs. Viewing Angle")

    # Add hover functionality
    cursor = mplcursors.cursor(high, hover=True)

    @cursor.connect("add")
    def on_add(sel):
        index = sel.index
        sel.annotation.set(text=f'{labels_5[index]}')
        sel.annotation.get_bbox_patch().set(fc="white")

    plt.show()


if __name__ == '__main__':
    input_path = r"/grb/resources/grbs_laio_2024.txt"

    grb_list = parser.parse(txt.read(input_path))
    plot_viewing_angles(grb_list)
