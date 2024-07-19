import math

import mplcursors
from matplotlib import pyplot as plt

from grb.parsers.liao import Liao
from grb.parsers.ryan import Ryan


"""
    Plotter.py
"""


def plot(grbs: list):
    """ Plots the SNR vs. viewing angle.

        Confidence Levels:
            - High: sigma >= 5
            - Mild: 3 <= sigma < 5
            - Low: sigma < 3
        """
    snr_0, lower_0, labels_low = [], [], []
    snr_3, lower_3, labels_3 = [], [], []
    snr_5, lower_5, labels_5 = [], [], []

    for grb in grbs:
        snr = math.degrees(grb.viewing.value) / math.degrees(grb.viewing.lower)
        viewing = math.degrees(grb.viewing.value)

        label = grb.id + '(' + str(round(viewing, 2)) + ',' + str(round(snr, 2)) + ')'

        if grb.off_axis_confidence >= 5.0:
            labels_5.append(label)
            snr_5.append(snr)
            lower_5.append(viewing)
        elif grb.off_axis_confidence >= 3.0:
            labels_3.append(label)
            snr_3.append(snr)
            lower_3.append(viewing)
        else:
            labels_low.append(label)
            snr_0.append(snr)
            lower_0.append(viewing)

    fig, ax = plt.subplots()

    # Plot High Confidence Angles
    high = ax.scatter(lower_5, snr_5, color='green', label='High Confidence')

    # Plot Mild Confidence Angles
    mild = ax.scatter(lower_3, snr_3, color='purple', label='Mild Confidence')

    # Plot Low Confidence Angles
    low = ax.scatter(lower_0, snr_0, color='black', label='Low Confidence')

    ax.legend()
    ax.set_ylabel("Viewing Angle (degrees) / Lower Bound (degrees)")
    ax.set_xlabel("Viewing Angle (degrees)")
    ax.set_title("Combined SNR vs. Viewing Angle")

    # Add hover functionality
    cursor = mplcursors.cursor(high, hover=True)

    @cursor.connect("add")
    def on_add(sel):
        index = sel.index
        sel.annotation.set(text=f'{labels_5[index]}')
        sel.annotation.get_bbox_patch().set(fc="white")

    plt.show()


if __name__ == '__main__':
    ryan = Ryan(r"C:\Projects\repos\grb\grb\resources\grbs_ryan_2015.txt")
    liao = Liao(r"C:\Projects\repos\grb\grb\resources\grbs_laio_2024.txt")

    grb_ids = []
    duplicates = []

    for liao_grb in liao.grbs:
        grb_ids.append(liao_grb.id)

    for ryan_grb in ryan.grbs:
        if ryan_grb.id in grb_ids:
            duplicates.append(ryan_grb.id)
        else:
            grb_ids.append(ryan_grb.id)

    grbs = []

    for liao_grb in liao.grbs:
        grbs.append(liao_grb)

    for ryan_grb in ryan.grbs:
        if ryan_grb.id not in duplicates:
            grbs.append(ryan_grb)

    plot(grbs)




