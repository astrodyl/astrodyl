import os

"""
    Text.py

    Collection of utility methods for interacting with text files.
"""


def read(path: str) -> list:
    """ Reads the file at specified path and returns its contents.

    :param path: path to file.
    :return: list of strings containing file data
    """
    with open(path) as f:
        return f.readlines()


def write(path: str, lines: list, clobber: bool = True) -> None:
    """ Writes file to disk. Will overwrite existing file if it already
    exists.

    :param path: destination to write file.
    :param lines: lines to write to the file.
    :param clobber: whether to overwrite an existing file
    """
    if os.path.exists(path) and not clobber:
        raise IOError(f"File {path} already exists.")

    with open(path, 'w') as f:
        for line in lines:
            f.write(line)
