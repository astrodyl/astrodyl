import os
import matplotlib.pyplot as plt

from grb.utils.io import txt


"""
    XRT.py

    The X-Ray Telescope (XRT) class parses XRT light curve files and
    plots the resulting light curve. AN option is available to plot
    either the Windowed Timing (WT) data, the Photon Counting (PC)
    data, or both. To manually ignore certain data, place an `!` at
    the start of the row containing the undesirable data.

    Data archive: https://www.swift.ac.uk/xrt_products/
    Data description: https://www.swift.ac.uk/xrt_curves/docs.php#products
"""


class XRTDataMode:
    """ Swift's XRT has multiple data modes (e.g., photon counting,
    windowed timing) each of which contain the same type of data.
    """
    def __init__(self):
        self.times: list = []
        self.time_lowers: list = []
        self.time_uppers: list = []

        self.fluxes: list = []
        self.flux_lowers: list = []
        self.flux_uppers: list = []


class XRT:
    def __init__(self, path: str):
        self.path = path
        self.data = txt.read(path)
        self.event = self.get_event()
        self.photon_counting = XRTDataMode()
        self.windowed_timing = XRTDataMode()

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

    def plot(self, wt: bool = False, pc: bool = True) -> None:
        """ Plots the XRT data.

        :param wt: plot the Windowed Timing data
        :param pc: plot the Photon Counting data
        """
        if wt and pc:
            data_used = '(WT + PC)'
            times = self.windowed_timing.times + self.photon_counting.times
            fluxes = self.windowed_timing.fluxes + self.photon_counting.fluxes
            y_error_lowers = self.windowed_timing.flux_lowers + self.photon_counting.flux_lowers
            y_error_uppers = self.windowed_timing.flux_uppers + self.photon_counting.flux_uppers
        elif wt:
            data_used = '(WT)'
            times = self.windowed_timing.times
            fluxes = self.windowed_timing.fluxes
            y_error_lowers = self.windowed_timing.flux_lowers
            y_error_uppers = self.photon_counting.flux_uppers
        elif pc:
            data_used = '(PC)'
            times = self.photon_counting.times
            fluxes = self.photon_counting.fluxes
            y_error_lowers = self.photon_counting.flux_lowers
            y_error_uppers = self.photon_counting.flux_uppers
        else:
            return

        plt.errorbar(times, fluxes, yerr=(y_error_lowers, y_error_uppers), fmt='.', color='royalblue', ecolor='black')
        plt.title(f'Swift/XRT Flux Curve of {self.event} ' + data_used)
        plt.xlabel('Time since BAT trigger (s)')
        plt.ylabel('Flux (0.3 - 10keV) (erg/cm^2/s)')
        plt.xscale('log')
        plt.yscale('log')

        plt.show()

    def get_event(self):
        return os.path.basename(os.path.dirname(self.path))


if __name__ == '__main__':
    input_path = r"C:\Projects\repos\grb\grb\resources\grbs\GRB140506A\xrt.txt"

    xrt = XRT(input_path)
    xrt.parse()
    xrt.plot(wt=True, pc=True)

