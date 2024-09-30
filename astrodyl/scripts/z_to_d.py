import numpy as np
from scipy.integrate import quad


class Distance:
    def __init__(self, cmd: float, ld: float):
        self.comoving = cmd
        self.luminosity = ld


def convert_redshift_to_distance(z: float, h0: float = 71, o_m: float = 0.3, o_l: float = 0.7, o_k: float = 0):
    """

    :param z: redshift
    :param h0: Hubble's constant at redshift = 0
    :param o_m: density of matter (omega_matter)
    :param o_l: density of dark matter (omega_lambda)
    :param o_k: curvature density (0 = flat)
    :return:
    """
    def e(rs: float) -> float:
        """ Calculates the dimensionless Hubble Parameter

        :param rs: redshift
        """
        return np.sqrt(o_m * (1 + rs) ** 3 + o_k * (1 + rs) ** 2 + o_l)

    def comoving_distance() -> float:
        """ Calculates the distance between two objects which remains
        constant with epoch if the two objects are moving with the Hubble
        flow. In other words, it is the distance between them which would
        be measured with rulers at the time they are being observed (the
        proper distance) divided by the ratio of the scale factor of the
        Universe then to now.

        See: https://ned.ipac.caltech.edu/level5/Hogg/Hogg4.html
        """
        return (3e5 / h0) * quad(lambda z_prime: 1 / e(z_prime), 0, z)[0]

    def luminosity_distance() -> float:
        """ Calculate the luminosity distance """
        return comoving_distance() * (1 + z)

    return Distance(comoving_distance(), luminosity_distance())


if __name__ == '__main__':
    redshift = 1
    distance = convert_redshift_to_distance(redshift)

    print(f"Comoving Distance at z = {redshift}:\t\t {distance.comoving:.2f} Mpc")
    print(f"Luminosity Distance at z = {redshift}:\t {distance.luminosity:.2f} Mpc")
