"""
Helper functions
"""


def read_to_list(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        file_contents = f.read().splitlines()
    return file_contents
