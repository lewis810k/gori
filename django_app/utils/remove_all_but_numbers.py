import re


def remove_non_numeric(string):
    all_numeric = re.sub("[^0-9]", "", string)
    return all_numeric
