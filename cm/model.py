import math
from matplotlib import pyplot as plt

from cm.definitions.hardware.filter import Filter
from cm.definitions.hardware.telescope import Telescope
from cm.definitions.parameters import Parameters
from cm.definitions.transient import Transient
from cm.definitions.hardware.hardware import Hardware


class Model:
    def __init__(self, transient: Transient, hardware: Hardware, params: Parameters,
                 snr: float, correction: float = None):

        self.transient: Transient = transient
        self.hardware: Hardware = hardware
        self.reference_parameters: Parameters = params
        self.correction_factor = correction
        self.desired_snr = snr

    def get_snr_dependence(self) -> float:
        """ Returns the signal-to-noise ratio factor for a desired SNR.
        Assumes that the noise is purely Poisson such that is proportional
        to sqrt(number of counts).

        :return: contribution of the signal-to-noise dependence
        """
        return (self.desired_snr / 5.0) ** 2.0

    def get_hardware_dependence(self) -> float:
        """ Returns the contribution due to the hardware efficiencies.
        Filter efficiencies are stored as a value between 0.0 and 1.0,
        while the telescope efficiencies are stored as an inverse such
        that the values are between 1.0 and 0.0.

        :return: contribution of the hardware efficiencies
        """
        if self.hardware.telescope.efficiency == 0:
            raise ValueError("Telescopes cannot have a 0 efficiency.")

        open_filter_efficiency = 0.00929728
        return ((self.hardware.filter.efficiency / open_filter_efficiency) /
                self.hardware.telescope.efficiency)

    def get_zero_point_dependence(self) -> float:
        """ Returns the zero point contribution

        :return: contribution of the filter zero point dependencies
        """
        return self.hardware.filter.zero_point / self.reference_parameters.filter.zero_point

    def get_temporal_dependence(self, time: float) -> float:
        """ Calculates the temporal contribution

        :param time: number of seconds since the transient trigger time
        :return: contribution of the temporal dependence
        """
        return (((time - self.transient.trigger_time) / self.reference_parameters.time)
                ** self.transient.temporal_index)

    def get_spectral_dependence(self) -> float:
        """ Calculates the spectral contribution

        :return:
        """
        return ((self.hardware.filter.frequency / self.reference_parameters.filter.frequency)
                ** self.transient.spectral_index)

    def get_extinction_dependence(self, r_v: float = 3.1) -> float:
        """ Calculates the dust extinction contribution for the extinguished
        power law model.

        :param r_v:  ???
        :return: contribution of the dust extinction dependence
        """
        x = 1.0 / self.hardware.filter.wavelength(um=True)
        y = x - 1.82
        a, b = 0.0, 0.0

        # Infrared
        if 0.3 <= x <= 1.1:
            a = 0.574 * x ** 1.61
            b = -0.527 * x ** 1.61

        # Optical/NIR
        elif 1.1 < x <= 3.3:
            a = (1 + 0.17699 * y - 0.50447 * y ** 2 - 0.02427 * y ** 3 +
                 0.72085 * y ** 4 + 0.01979 * y ** 5 - 0.7753 * y ** 6 + 0.32999 * y ** 7)
            b = (1.41338 * y + 2.28305 * y ** 2 + 1.07233 * y ** 3 -
                 5.38434 * y ** 4 - 0.62251 * y ** 5 + 5.3026 * y ** 6 - 2.09002 * y ** 7)

        return r_v * self.transient.ebv * (a + b / r_v)

    def magnitude(self, time: float):
        """ Models the magnitude at the provided time given the reference
        parameters.

        :param time: number of seconds since the transient trigger time
        :return: Modeled magnitude at the provided time
        """
        return (self.reference_parameters.magnitude -
                (2.5 * (math.log10(self.get_temporal_dependence(time))
                        + math.log10(self.get_spectral_dependence())
                        - math.log10(self.get_zero_point_dependence())))
                + self.get_extinction_dependence())

    def exposure_length(self, time: float, magnitude: float = None) -> float:
        """ Calculates the exposure length for a given time and desired SNR
        using the defined model parameters.

        :param time: number of seconds since the transient trigger time
        :param magnitude: optional magnitude if already known
        :return: exposure length in seconds
        """
        if magnitude is None:
            magnitude = self.magnitude(time)

        return (self.get_snr_dependence() * self.get_hardware_dependence()
                * (10.0 ** ((magnitude - 20.0) / 2.5)) * (self.correction_factor or 1.0))


if __name__ == '__main__':

    # Define the transient parameters
    transient = Transient(0.0, a=-1, b=-0.7, ebv=0.0)

    # Define the hardware
    filter_ = Filter('B', 688703000000000.0, 0.0583863, 4.06300)
    telescope = Telescope('P5', 0.237073)
    hardware = Hardware(filter_, telescope)

    # Define the reference parameters
    reference_filter = Filter('R', 472188000000000.0, 0.0379989, 3.06400)
    parameters = Parameters(reference_filter, 3600.0, 20.0)

    # Define the model
    afterglow_model = Model(transient, hardware, parameters, 10.0)

    # Calculate the exposure lengths
    times = [float(i) for i in range(1, 3601, 1)]
    magnitudes = [afterglow_model.magnitude(time) for time in times]
    exposure_lengths = [afterglow_model.exposure_length(time) for time in times]

    print(magnitudes)

    fig, ax = plt.subplots()
    ax.plot([time / 60.0 for time in times], exposure_lengths, label='B', color='blue')

    # Define additional filters
    filters = [
        Filter('V', 547266000000000.0, 0.0564145, 3.63600),
        Filter('R', 472188000000000.0, 0.0379989, 3.06400),
        Filter('I', 374741000000000.0, 0.0435316, 2.41600)
    ]

    colors = ['green', 'red', 'darkblue']

    # Plot additional filters
    for i, f in enumerate(filters):
        afterglow_model.hardware.filter = f
        ax.plot([time / 60.0 for time in times], [afterglow_model.exposure_length(time) for time in times],
                label=f.name, color=colors[i])

    ax2 = ax.twiny()
    flux_ticks = ax.get_xticks()
    afterglow_model.hardware.filter = filters[1]
    flux_ticks2 = []
    for tick in flux_ticks:
        if tick <= 0.0:
            flux_ticks2.append(1)
        else:
            flux_ticks2.append(tick)

    # Displays magnitude in I band
    magnitude_ticks = [afterglow_model.magnitude(flux_tick * 60.0) for flux_tick in flux_ticks2]
    ax2.set_xticks(flux_ticks2)
    ax2.set_xticklabels([f'{mag:.2f}' for mag in magnitude_ticks])
    ax2.set_xlabel('Magnitude')
    ax2.tick_params(axis='x')

    ax.set_xlabel('Time Since Trigger (Minutes)')
    ax.set_ylabel('Exposure Length (s)')
    ax.legend()
    plt.show()
