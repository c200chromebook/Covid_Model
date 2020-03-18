import re


def parse_tuple_list(list_of_tuples):
    return [tuple(state.strip('()').split(',')) for state in re.findall(r'(\([\w\.\-\d]+,[.\d]+\))', list_of_tuples)]
