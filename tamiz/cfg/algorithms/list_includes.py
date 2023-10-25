from typing import List


def list_includes(superlist: List[str], sublist: List[str]) -> bool:
    """
    Check that each of the elements of a sublist, at least ones enters into the superlist.
    Supports duplicated elements (twice in sublist should be twice in superlist)
    Ignores the order.
    Args:
        superlist:
        sublist:

    Returns: True or False

    """
    from collections import Counter
    counter_sub = Counter(sublist)
    counter_sup = Counter(superlist)
    for item, count in counter_sub.items():
        if count > counter_sup[item]:
            return False
    return True


def is_sublist(superlist: List[str], sublist: List[str]) -> bool:
    """
    Currently not used.
    Searches if sublist is entering the superlist as is (in case of strings would be equivalent
    to the search of a substring)
    Args:
        superlist:
        sublist:

    Returns:

    """
    if len(sublist) > len(superlist):
        return False

    idx1, idx2 = 0, 0

    while idx1 < len(superlist) and idx2 < len(sublist):
        if superlist[idx1] == sublist[idx2]:
            idx2 += 1
        idx1 += 1

    return idx2 == len(sublist)
