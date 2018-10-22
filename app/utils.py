from almuerbot.base import Session
from almuerbot.exceptions import AlreadyExistsException


def get(session=None, table=None, filterdict={}, amount=10):
    _session = session or Session()
    conditions = []
    for attr_name, value in filterdict.items():
        if value is not None:
            conditions.append(getattr(table, attr_name) == value)
    ret_values = _session.query(table).filter(*conditions).limit(amount)
    if not session:
        _session.close()
    return list(map(lambda x: x.__as_dict__(), ret_values))


def add(
        session=None,
        table=None,
        data={}):
    """Add data to table."""
    _session = session or Session()
    _session.add(table(**data))
    _session.commit()
    if not session:
        session.close()


def check(
        session=None,
        table=None,
        conditiondict={}):
    """Check if value is in table."""
    _session = session or Session()
    conditions = []
    for key, value in conditiondict.items():
        conditions.append(getattr(table, key) == value)
    compatible = _session.query(table).filter(*conditions)
    if not session:
        _session.close()
    return bool([a for a in compatible])


def add_if_not_exists(
        session=None,
        table=None,
        unique_attr_key=None,
        unique_attr_value=None,
        data={}):
    """Add data to table."""
    _session = session or Session()
    if not check(
            session=_session,
            table=table,
            conditiondict={unique_attr_key: unique_attr_value}):
        add(session=_session, table=table, data=data)


def delete(
        session=None,
        table=None,
        data={}):
    """Delete from table."""
    _session = session or Session()
    _session.delete(table(**data))
    _session.commit()
    if not session:
        session.close()


def to_snake(string):
    return string.lower().replace(' ', '_')
