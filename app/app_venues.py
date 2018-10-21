from utils import random_from_list


def get_venues(venues, id=None, name=None, amount=10):
    """Return user dict."""
    if id is not None:
        return [a for a in users if a['id'] == int(id)][0]
    elif name is not None:
        return [a for a in users if a['name'].lower() == name.lower()][0]
    else:
        return random_from_list(venues, amount)


def add_venues(venues, id, name, distance, url):
    """Add user to db."""
    venues.append({
        'id': id,
        'name': name,
        'distance': distance,
        'url': url})
