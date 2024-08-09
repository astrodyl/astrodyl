from datetime import datetime, timedelta


class Date:
    def __init__(self, mjd: float = None, utc: str | datetime = None):
        self.epoch = datetime(1858, 11, 17)

        if mjd:
            self.mjd = mjd
            self.utc = self.epoch + timedelta(days=self.mjd)

        elif utc:
            if isinstance(utc, str):
                self.utc = datetime.strptime(utc, "%Y-%m-%d %H:%M:%S.%f")
            elif isinstance(utc, datetime):
                self.utc = utc

            self.mjd = (self.utc - self.epoch).total_seconds() / 86400.0

    def __sub__(self, other) -> float:
        """ Defines the subtraction between two Date objects.

        :param other: Date object that will be subtracted
        :return: difference in days between Date objects
        """
        if not isinstance(other, Date):
            return NotImplemented

        return round((self.mjd - other.mjd), 5)


if __name__ == "__main__":

    # [ Example UTC Usage ]
    trigger_date = Date(utc="2009-06-18 08:28:29.0")
    exposure_date = Date(utc="2009-06-18 20:28:29.0")

    # Number of seconds since trigger
    print((exposure_date - trigger_date) * 86400.0)

    # [ Example MJD Usage ]
    trigger_time = Date(mjd=60531.4581)
    exposure_time = Date(mjd=60532.45831)

    # Number of days since trigger
    print((exposure_time - trigger_time))
