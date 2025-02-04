import os
import matplotlib.pyplot as plt

from astrodyl.core.utils.xrt_data_mode import XRTDataMode
from astrodyl.core.io import txt

"""
    xrt.py

    The X-Ray Telescope (XRT) class parses XRT light curve files and
    plots the resulting light curve. AN option is available to plot
    either the Windowed Timing (WT) data, the Photon Counting (PC)
    data, or both. To manually ignore certain data, place an `!` at
    the start of the row containing the undesirable data.

    Data archive: https://www.swift.ac.uk/xrt_products/
    Data description: https://www.swift.ac.uk/xrt_curves/docs.php#products
"""


class XRT:
    def __init__(self, path: str, event: str):
        self.path = path
        self.data = txt.read(path)
        self.photon_counting = XRTDataMode()
        self.windowed_timing = XRTDataMode()
        self.event = event

        self.wt_start = None
        self.pc_start = None

    def parse(self) -> None:
        """ Parse XRT's data from the standard text file.

        Column schema:
            - Time
            - Time positive error
            - Time negative error
            - Source count rate
            - Positive error in count rate (1-σ)
            - Negative error in count rate (1-σ)
        """
        self.find_modes()
        self.parse_mode(self.windowed_timing, self.wt_start, self.pc_start)
        self.parse_mode(self.photon_counting, self.pc_start, len(self.data) - 1)

    def find_modes(self) -> None:
        """ Finds the starting point of each data mode. Raises a ValueError
        exception if the WT or PC data could not be found.
        """
        for i, line in enumerate(self.data):
            if line.startswith('READ') or line.startswith('NO'):
                continue

            self.get_mode_start(line, i)

        if self.wt_start is None or self.pc_start is None:
            raise ValueError(f"Missing data for {self.event}.")

    def parse_mode(self, mode: XRTDataMode, start: int, stop: int) -> None:
        """ Parses the data for a provided range corresponding to a
        data mode.

        :param mode: XRTDataMode object
        :param start: starting index
        :param stop: stopping index
        """
        for i in range(start, stop):
            row = self.data[i]

            if row.startswith('READ') or row.startswith('NO') or row.startswith('!'):
                continue

            data = row.split('\t')

            mode.times.append(float(data[0]))
            mode.time_uppers.append(abs(float(data[1])))
            mode.time_lowers.append(abs(float(data[2])))

            mode.fluxes.append(float(data[3]))
            mode.flux_uppers.append(abs(float(data[4])))
            mode.flux_lowers.append(abs(float(data[5])))

    def get_mode_start(self, line: str, index: int) -> None:
        """ Determines the starting point of the WT and PC data modes.

        :param line: line to check for data mode comment
        :param index: line index
        """
        if line.startswith('!'):
            mode = line.replace('!', '').strip()

            if mode == 'WT':
                self.wt_start = index + 1
            elif mode == 'PC_incbad':
                self.pc_start = index + 1

    def plot(self, wt: bool = True, pc: bool = True) -> None:
        """ Plots the XRT data.

        :param wt: plot the Windowed Timing data
        :param pc: plot the Photon Counting data
        """
        if wt:
            plt.errorbar(self.windowed_timing.times, self.windowed_timing.fluxes,
                         yerr=(self.windowed_timing.flux_lowers, self.windowed_timing.flux_uppers),
                         fmt='.', color='royalblue', ecolor='black', label='Windowed Timing')

        if pc:
            plt.errorbar(self.photon_counting.times, self.photon_counting.fluxes,
                         yerr=(self.photon_counting.flux_lowers, self.photon_counting.flux_uppers),
                         fmt='.', color='purple', ecolor='black', label='Photon Counting')

        if wt or pc:
            plt.title(f'Swift XRT Flux Curve of {self.event}')
            plt.xlabel('Time since BAT trigger (s)')
            plt.ylabel('Flux (0.3 - 10keV) (erg/cm^2/s)')
            plt.xscale('log')
            plt.yscale('log')
            plt.legend()

            plt.show()


if __name__ == '__main__':
    # input_path = os.path.join(os.getcwd(), 'grb', r"resources/grbs/GRB_140506A/xrt.txt")
    input_path = os.path.join(r"/grb/resources/grbs/GRB_160131A/xrt.txt")

    xrt = XRT(input_path, event='160131A')
    xrt.parse()
    xrt.plot(wt=True, pc=True)

