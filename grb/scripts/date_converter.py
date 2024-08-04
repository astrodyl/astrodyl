from datetime import datetime, timedelta


def calculate_days_since(date1_str, date2_str):
    # Define the date format
    date_format = "%Y-%m-%d %H:%M:%S.%f"

    # Parse the date strings into datetime objects
    date1 = datetime.strptime(date1_str, date_format)
    date2 = datetime.strptime(date2_str, date_format)

    # Return the difference in days
    return (date2 - date1).total_seconds() / 86400.0


def mjd_to_datetime(mjd):
    # The MJD epoch starts at midnight on November 17, 1858
    mjd_epoch = datetime(1858, 11, 17, 0, 0, 0)

    # Calculate the difference in days from the MJD epoch
    delta = timedelta(days=mjd)

    # Add the delta to the epoch to get the datetime
    return mjd_epoch + delta


def print_results():
    print(f"[ GCN {gcn} ]")
    print(f"Trigger date........ {trigger_date}")
    print(f"Observation date.... {obs_date}")
    print(f"Delta days.......... {round(delta_days, 6)}\n")


if __name__ == "__main__":

    # GRB 080319B
    trigger_date = "2009-06-18 08:28:29.0"

    gcn = 9576
    obs_date = '2009-06-18 22:08:00.0'
    delta_days = calculate_days_since(trigger_date, obs_date)
    print_results()

