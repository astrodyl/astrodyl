from typing import List

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

from cm.definitions.hardware.filter import Filter
from cm.definitions.hardware.hardware import Hardware
from cm.definitions.hardware.telescope import Telescope
from cm.definitions.parameters import Parameters
from cm.definitions.transient import Transient
from cm.model import Model


class Viewer:
    def __init__(self, times: list):
        # Figure Parameters
        self.ax = None
        self.ax2 = None
        self.figure = None
        self.b_filter_line = None
        self.v_filter_line = None
        self.r_filter_line = None
        self.i_filter_line = None

        # Model Parameters
        self.model = None
        self.times = times

        # Buttons
        self.button_reset = None
        self.button_tele_p5 = None
        self.button_tele_mo = None
        self.button_b_mag = None
        self.button_v_mag = None
        self.button_r_mag = None
        self.button_i_mag = None

        # Sliders
        self.slider_temporal = None
        self.slider_spectral = None
        self.slider_ref_time = None
        self.slider_ref_mag = None
        self.slider_v_mag = None

        # Markers
        self.marker_v_mag = None

        # Supported Telescopes and Filters
        self.filters = {
            'B': Filter('B', 688703e9, 0.0583863, 4.06300),
            'V': Filter('V', 547266e9, 0.0564145, 3.63600),
            'R': Filter('R', 472188e9, 0.0379989, 3.06400),
            'I': Filter('I', 374741e9, 0.0435316, 2.41600),
        }

        self.telescopes = {
            'P5': Telescope('P5', 0.237073),
            'MO': Telescope('MO', 0.196503),
        }

        self.init()

    # <editor-fold desc="Constructors">
    def init(self) -> None:
        """ Constructs the model and figure """
        self.init_model()
        self.init_figure()

    def init_model(self) -> None:
        """ Initializes the default model to be viewed """
        self.model = Model(
            transient=Transient(0.0, a=-1.0, b=-0.7, ebv=0.0),
            hardware=Hardware(self.filters['B'], self.telescopes['P5']),
            params=Parameters(self.filters['R'], time=3600.0, magnitude=20.0),
            snr=10.0
        )

    def init_figure(self) -> None:
        """ Initializes the figure """
        self.figure, self.ax = plt.subplots(figsize=(15, 10))
        plt.subplots_adjust(left=0.1, bottom=0.4)

        self.init_sliders()
        self.init_buttons()
        self.init_lines()

    def init_buttons(self) -> None:
        """ Initializes the buttons """
        self.button_reset = Button(plt.axes((0.91, 0.8, 0.08, 0.08)), 'Reset',
                                   color='cornflowerblue', hovercolor='royalblue')
        self.button_tele_p5 = Button(plt.axes((0.91, 0.7, 0.08, 0.08)), 'PROMPT-5',
                                     color='orchid', hovercolor='mediumvioletred')
        self.button_tele_mo = Button(plt.axes((0.91, 0.6, 0.08, 0.08)), 'PROMPT-MO',
                                     color='lightcoral', hovercolor='indianred')

        self.button_reset.on_clicked(self.on_reset_click)
        self.button_tele_p5.on_clicked(self.on_tele_p5_click)
        self.button_tele_mo.on_clicked(self.on_tele_mo_click)

        # Display buttons that toggle between magnitude and exposure length
        self.button_b_mag = Button(plt.axes((0.91, 0.52, 0.08, 0.03)), 'B Mag =',
                                   color='white', hovercolor='white')
        self.button_v_mag = Button(plt.axes((0.91, 0.48, 0.08, 0.03)), 'V Mag =',
                                   color='white', hovercolor='white')
        self.button_r_mag = Button(plt.axes((0.91, 0.44, 0.08, 0.03)), 'R Mag =',
                                   color='white', hovercolor='white')
        self.button_i_mag = Button(plt.axes((0.91, 0.40, 0.08, 0.03)), 'I Mag =',
                                   color='white', hovercolor='white')
        self.update_mag_buttons()

        self.button_b_mag.on_clicked(self.on_b_mag_click)
        self.button_v_mag.on_clicked(self.on_v_mag_click)
        self.button_r_mag.on_clicked(self.on_r_mag_click)
        self.button_i_mag.on_clicked(self.on_i_mag_click)

    def init_lines(self) -> None:
        """ Initializes the modeled exposure length lines """
        minutes = [time / 60.0 for time in self.times]
        self.b_filter_line, = self.ax.plot(minutes, self.get_exposure_lengths('B'), label='B', color='blue')
        self.v_filter_line, = self.ax.plot(minutes, self.get_exposure_lengths('V'), label='V', color='green')
        self.r_filter_line, = self.ax.plot(minutes, self.get_exposure_lengths('R'), label='R', color='red')
        self.i_filter_line, = self.ax.plot(minutes, self.get_exposure_lengths('I'), label='I', color='darkblue')

    def init_sliders(self) -> None:
        """ Initializes the model parameter sliders"""
        self.slider_v_mag = Slider(plt.axes((0.135, 0.3, 0.73, 0.01)), '', 0., self.times[-1]//60,
                                   facecolor='skyblue', track_color='steelblue', valinit=self.times[-1] // 120)
        self.slider_temporal = Slider(plt.axes((0.2, 0.2, 0.7, 0.03)), 'Temporal Index', -3., 3.,
                                      facecolor='skyblue', track_color='steelblue', valinit=-1.0)
        self.slider_spectral = Slider(plt.axes((0.2, 0.15, 0.7, 0.03)), 'Spectral Index', -3., 3.,
                                      facecolor='skyblue', track_color='steelblue', valinit=-0.7)
        self.slider_ref_time = Slider(plt.axes((0.2, 0.1, 0.7, 0.03)), 'Reference Time', 1., 120.,
                                      facecolor='skyblue', track_color='steelblue', valinit=60.)
        self.slider_ref_mag = Slider(plt.axes((0.2, 0.05, 0.7, 0.03)), 'Reference Mag', 0., 30.,
                                     facecolor='skyblue', track_color='steelblue', valinit=20.)

        # Assign event handlers
        self.slider_v_mag.on_changed(self.on_v_mag_update)
        self.slider_temporal.on_changed(self.on_temporal_update)
        self.slider_spectral.on_changed(self.on_spectral_update)
        self.slider_ref_time.on_changed(self.on_reference_time_update)
        self.slider_ref_mag.on_changed(self.on_reference_magnitude_update)
        self.init_v_mag_slider()  # This slider is unique

    def init_v_mag_slider(self) -> None:
        """ Initializes the V mag slider. The slider moves a point along
        the V band line and calculates the magnitude at that point. The
        magnitude is then displayed in separate button.
        """
        self.model.hardware.filter = self.filters['V']
        exp_length = self.model.exposure_length(self.times[-1] // 2, self.model.magnitude(self.times[-1] // 2))

        self.marker_v_mag, = self.ax.plot(self.times[-1] // 120, exp_length, marker='o', color='green', markersize=10)
    # </editor-fold>

    def show(self):
        """ Displays the figure """
        self.ax.set_xlabel('Time Since Trigger (Minutes)')
        self.ax.set_ylabel('Exposure Length (s)')
        self.ax.set_title('Campaign Manager\'s Afterglow Model')
        self.ax.legend()
        plt.show()

    def update(self) -> None:
        """ """
        self.update_lines()
        self.update_v_mag_marker(self.slider_v_mag.val * 60.0)
        self.update_mag_buttons()
        self.figure.canvas.draw_idle()

    # <editor-fold desc="Button Updaters">
    def on_b_mag_click(self, event) -> None:
        """ """
        self.toggle_button_label(self.button_b_mag, self.slider_v_mag.val * 60.0, 'B')

    def on_v_mag_click(self, event) -> None:
        """ """
        self.toggle_button_label(self.button_v_mag, self.slider_v_mag.val * 60.0, 'V')

    def on_r_mag_click(self, event) -> None:
        """ """
        self.toggle_button_label(self.button_r_mag, self.slider_v_mag.val * 60.0, 'R')

    def on_i_mag_click(self, event) -> None:
        """ """
        self.toggle_button_label(self.button_i_mag, self.slider_v_mag.val * 60.0, 'I')

    def toggle_button_label(self, button, time: float, band: str) -> None:
        """ """
        if 'Mag' in button.label.get_text():
            exp_len = round(self.get_exposure_length(time, band), 2)
            button.label.set_text(f"{band} Len = {exp_len}s")

        elif 'Len' in button.label.get_text():
            mag = round(self.get_magnitude(time, band), 2)
            button.label.set_text(f'{band} Mag = {mag}')

        self.figure.canvas.draw_idle()

    def on_reset_click(self, event) -> None:
        """ Resets all the sliders and redraws the plot """
        self.model.hardware.telescope = self.telescopes['P5']
        self.slider_temporal.reset()
        self.slider_spectral.reset()
        self.slider_ref_time.reset()
        self.slider_ref_mag.reset()
        self.slider_v_mag.reset()
        self.update()

    def on_tele_p5_click(self, event) -> None:
        """ Updates the model using values for the PROMPT-5 telescope """
        print(f"Set Telescope Efficiency to match PROMPT-5: {self.telescopes['P5'].efficiency}")
        self.model.hardware.telescope = self.telescopes['P5']
        self.update()

    def on_tele_mo_click(self, event) -> None:
        """ Updates the model using values for the PROMPT-MO telescope """
        print(f"Set Telescope Efficiency to match PROMPT-MO: {self.telescopes['MO'].efficiency}")
        self.model.hardware.telescope = self.telescopes['MO']
        self.update()

    def update_button_label(self, button, time: float, band: str) -> None:
        """ Updates the button label depending on which display is active. """
        if 'Mag' in button.label.get_text():
            mag = round(self.get_magnitude(time, band), 2)
            button.label.set_text(f'{band} Mag = {mag}')
        elif 'Len' in button.label.get_text():
            exp_len = round(self.get_exposure_length(time, band), 2)
            button.label.set_text(f'{band} Len = {exp_len}s')

    def update_mag_buttons(self) -> None:
        """ Updates the magnitude buttons. Checks if they are toggled
        between magnitude and exposure length.
        """
        if 'B' in self.button_b_mag.label.get_text():
            self.update_button_label(self.button_b_mag, self.slider_v_mag.val * 60.0, 'B')
        if 'R' in self.button_r_mag.label.get_text():
            self.update_button_label(self.button_r_mag, self.slider_v_mag.val * 60.0, 'R')
        if 'I' in self.button_i_mag.label.get_text():
            self.update_button_label(self.button_i_mag, self.slider_v_mag.val * 60.0, 'I')
        if 'V' in self.button_v_mag.label.get_text():
            self.update_button_label(self.button_v_mag, self.slider_v_mag.val * 60.0, 'V')
    # </editor-fold">

    # <editor-fold desc="Slider Updaters">
    def on_v_mag_update(self, val: float) -> None:
        """ Moves the V mag marker """
        if val <= 0:
            return

        self.marker_v_mag.set_xdata([val])
        self.update_v_mag_marker(val * 60.0)
        self.update_mag_buttons()

    def on_temporal_update(self, val: float) -> None:
        """ Updates the plot after a change to the temporal index slider """
        self.model.transient.temporal_index = self.slider_temporal.val
        self.update()

    def on_spectral_update(self, val: float) -> None:
        """ Updates the plot after a change to the spectral index slider """
        self.model.transient.spectral_index = self.slider_spectral.val
        self.update()

    def on_reference_magnitude_update(self, val: float) -> None:
        """ Updates the plot after a change to the reference magnitude slider """
        self.model.reference_parameters.magnitude = self.slider_ref_mag.val
        self.update()

    def on_reference_time_update(self, val: float) -> None:
        """ Updates the plot after a change to the reference time slider """
        self.model.reference_parameters.time = self.slider_ref_time.val * 60.0
        self.update()
    # </editor-fold>

    # <editor-fold desc="Other Updaters">
    def update_v_mag_marker(self, time: float) -> None:
        """ Moves the V band marker according to the model parameters.

        :param time: time in seconds since the trigger
        """
        self.model.hardware.filter = self.filters['V']
        self.marker_v_mag.set_ydata([self.model.exposure_length(time, self.model.magnitude(time))])

    def update_lines(self) -> None:
        """ Recalculates the exposure lengths and updates the plotted lines
        accordingly.
        """
        original_filter = self.model.hardware.filter

        self.b_filter_line.set_ydata(self.get_exposure_lengths('B'))
        self.v_filter_line.set_ydata(self.get_exposure_lengths('V'))
        self.r_filter_line.set_ydata(self.get_exposure_lengths('R'))
        self.i_filter_line.set_ydata(self.get_exposure_lengths('I'))

        self.model.hardware.filter = original_filter
    # </editor-fold>

    # <editor-fold desc="Getters">
    def get_exposure_lengths(self, filter_: str) -> List[float]:
        """ Returns the modeled exposure lengths in the provided filter
        band.

        :param filter_: filter name
        :return: list modeled exposure lengths
        """
        self.model.hardware.filter = self.filters[filter_]
        return [self.model.exposure_length(time) for time in self.times]

    def get_exposure_length(self, time: float, filter_: str, mag: float = None) -> float:
        """ Returns the exposure length at the provided time in the provided
        filter for the provided [optional] magnitude.

        :param time: time in seconds since the trigger
        :param filter_: filter name
        :param mag: magnitude of the of target
        :return: modeled exposure length in seconds
        """
        self.model.hardware.filter = self.filters[filter_]
        return self.model.exposure_length(time, mag)

    def get_magnitude(self, time: float, filter_: str) -> float:
        """ Returns the modeled magnitude at the provided time and for
        the provided filter band.

        :param time: time in seconds since the trigger
        :param filter_: filter name
        :return: modeled magnitude
        """
        self.model.hardware.filter = self.filters[filter_]
        return self.model.magnitude(time)
    # </editor-fold>


if __name__ == '__main__':
    viewer = Viewer(times=[float(i) for i in range(1, 7201, 2)])

    viewer.show()
