import json
import pandas as pd


def load_data(json_path: str, csv_path: str):
    """ Loads the Jet Break and GRB data """
    return load_json(json_path), load_excel(csv_path)


def load_json(path: str):
    """ Loads the Jet Break data """
    with open(path, 'r') as f:
        return json.load(f)


def load_excel(path: str):
    """ Loads teh GRB data """
    return pd.ExcelFile(path)


if __name__ == '__main__':
    # Criteria for keeping GRB events
    min_points, table = 10, {}

    # Load in the GRB photometry and XRT Break data
    break_data, grb_data = load_data(r"C:\Projects\repos\grb\grb\resources\break_times.json",
                                     r"C:\Users\Dylan\Documents\grb_final.xlsx")

    for sheet_name in grb_data.sheet_names:
        breaks_with_data = []

        # Read the data for a particular GRB event
        df = pd.read_excel(grb_data, sheet_name=sheet_name)

        for break_time in break_data[sheet_name]:
            before, after = 0, 0

            # Determine if the photometry is pre- or post-break
            for i, data_time in enumerate(df['days_since']):
                if (data_time * 86400.0) < break_time:
                    before += 1
                elif (data_time * 86400.0) > break_time:
                    after += 1

            # Store the information if it passes criteria
            if before >= min_points and after >= min_points:
                breaks_with_data.append((before, after))

        if breaks_with_data:
            table[sheet_name] = breaks_with_data

    print('\n')
    print(f'+---------------------------------------------------------+')
    print(f'| {len(table)} of {len(grb_data.sheet_names)} GRB events have at least {min_points} photometry points. |')
    print(f'+---------------------------------------------------------+')
