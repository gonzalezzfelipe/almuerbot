from utils import random_from_list


def get_users(users, id, username, email, amount=10):
    """Return user dict."""
    if id is not None:
        return [a for a in users if a['id'] == int(id)][0]
    elif username is not None:
        return [a for a in users if a['username'] == username][0]
    elif username is not None:
        return [a for a in users if a['email'] == email][0]
    else:
        return random_from_list(users, amount)


def add_user(users, id, username, name, email):
    """Add user to db."""
    users.append({
        'name': name,
        'email': email,
        'username': username,
        'id': id})
