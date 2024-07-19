import mplcursors
from matplotlib import pyplot as plt

from grb.parsers.liao.entry import GRB
from grb.utils.io import txt


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

    def plot(self):
        """ Plots the viewing angle confidence vs. viewing angle.

            Confidence Levels:
                - High: sigma >= 5
                - Mild: 3 <= sigma < 5
                - Low: sigma < 3
            """
        viewing, lower, labels_low = [], [], []
        viewing_3, lower_3, labels_3 = [], [], []
        viewing_5, lower_5, labels_5 = [], [], []

        for i, grb in enumerate(self.grbs):
            label = grb.id + '(' + str(grb.viewing.value) + ',' + str(grb.viewing.lower) + ')'

            if grb.off_axis_confidence >= 5.0:
                labels_5.append(label)
                viewing_5.append(grb.viewing.value)
                lower_5.append(grb.viewing.lower)
            elif grb.off_axis_confidence >= 3.0:
                labels_3.append(label)
                viewing_3.append(grb.viewing.value)
                lower_3.append(grb.viewing.lower)
            else:
                labels_low.append(label)
                viewing.append(grb.viewing.value)
                lower.append(grb.viewing.lower)

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
    input_path = r"C:\Projects\repos\grb\grb\resources\grbs_laio_2024.txt"

    sources = Liao(input_path)
    sources.plot()
