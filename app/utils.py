import random


def random_from_list(l, n):
    """Return n random items from list."""
    if len(l) <= n:
        return l
    else:
        return random.sample(l, n)
