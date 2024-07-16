from grb.utils.io import txt

"""
    Separator.py
    
    The Separator separates the lines of GRB list file based on each GRB's
    specified fields and specified bounds for easier viewing. Separate lists
    can be saved to new files.
    
    To separate by multiple fields, call the `separate` method for each field,
    passing the result to each new call and save the resulting file after the
    last call by calling `write_to_disk`. See the example in the main method.
    
    Supported fields:
        - Date
        - Viewing Angle
        - Opening Angle
        - Viewing Angle Confidence
        - Lorentz Boost
"""


def separate(lines: list, field: str, upper: float = None, lower: float = None, comment: str = '#'):
    """ Filters the lines of GRB list file based on specified field and specified bounds.

    :param lines: list of lines to be filtered
    :param field: field name
    :param upper: upper bound of field
    :param lower: lower bound of field
    :param comment: comment character
    :return: lines that are within the provided bounds
    """
    field = field.lower()

    if lower is None and upper is None:
        raise ValueError("No separating bounds were provided.")

    if field not in ['date', 'viewing angle', 'opening angle', 'viewing angle confidence', 'Lorentz Boost']:
        raise ValueError(f"Field not supported: {field}.")

    col = get_column(field)

    sep_lines = []
    for line in lines:
        if line.startswith(comment):
            sep_lines.append(line)
            continue

        if is_value_within_limits(line.split('\t')[col], field, upper, lower):
            sep_lines.append(line)

    return sep_lines


def is_value_within_limits(value: str, field: str, upper: float, lower: float):
    """ Determines if the value is within the specified bounds. Value can
    be a date of the form GRBYYMMDD, or a string representation of a float.

    :param value: str value to check.
    :param field: field name to check.
    :param upper: upper limit.
    :param lower: lower limit.
    :return: True if value within limits (inclusive).
    """
    if field in ['date']:  # Sanitize date to be convertable to float
        value = ''.join(char for char in value if char.isdigit())

    # We don't care about the bounds
    if '+' in value or '-' in value:
        value = value.split(' ')[0]

    if lower and float(value) < lower:
        return False

    if upper and float(value) > upper:
        return False

    return True


def get_column(field: str) -> int:
    """ Returns the integer column index corresponding to the specified
    field.

    :return: integer column index
    """
    if field == 'date':
        return 0
    if field == 'lorentz boost':
        return 2
    if field == 'viewing angle':
        return 3
    if field == 'opening angle':
        return 4
    if field == 'viewing angle confidence':
        return 5

    raise ValueError(f'Field {field} not recognized')


if __name__ == '__main__':
    """ Main entry point for separator """

    input_path = r"/grb/resources/grbs_laio_2024.txt"
    output_path = r"C:\Projects\repos\grb\grb\results\filtered_grbs.txt"

    content = txt.read(input_path)

    # Keep only GRBs with VAC of 3 and above
    separated_lines = separate(content, 'Viewing Angle Confidence', lower=3)

    # Keep only GRBs that occurred between 2012 and 2013
    separated_lines = separate(separated_lines, 'Date', upper=130000, lower=120000)

    # Add footer
    separated_lines.append(separated_lines[0])
    separated_lines.append(f'# Filtered by viewing angle confidence greater than 3 inclusive\n')
    separated_lines.append(f'# Filtered by date between Jan 1, 2012 and Jan 1, 2013 inclusive\n')
    separated_lines.append(separated_lines[0])

    txt.write(output_path, separated_lines)
