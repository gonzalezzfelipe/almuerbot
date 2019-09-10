import logging
from abc import ABC, abstractproperty

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from almuerbot.config import constants
from almuerbot.data.models import Rating, User, Venue, Group, Category


class Manager(ABC):
    """Base Manager object.

    Abstract base class to query the backend. For being "instanciable",
    one must define the `_model` property.
    """

    @abstractproperty
    def _model(self):
        """Object to query."""
        pass

    def __init__(self, db_uri=constants.DATABASE_URI):
        """Initialize almuerbot manager."""
        self.engine = create_engine(constants.DATABASE_URI)
        self.get_session = sessionmaker(bind=self.engine)

    def get(self, **filters):
        """Get all values that match filters."""
        session = filters.pop('session', False)
        conditions = []
        for attr_name, value in filters.items():
            if isinstance(value, list):
                conditions.append(getattr(self._model, attr_name).in_(value))
            if isinstance(value, tuple):
                conditions.append(
                    getattr(self._model, attr_name).between(*value))
            else:
                conditions.append(getattr(self._model, attr_name) == value)
        session = session or self.get_session()
        ret_values = session.query(self._model).filter(*conditions)
        session.close()
        return ret_values

    def get_first(self, **filters):
        """Get first matching value."""
        try:
            return self.get(**filters)[0]
        except IndexError:
            return None

    def get_by_id(self, id, session=None):
        """Get first matching value."""
        return self.get_first(id=id, session=session)

    def add(self, *args, **kwargs):
        """Add to database."""
        session = kwargs.pop('session', False)
        obj = self._model(*args, **kwargs)
        session = session or self.get_session()
        session.add(obj)
        session.commit()
        session.close()
        return obj

    def update(self, id, **kwargs):
        """Update row by id."""
        session = kwargs.pop('session', False)
        session = session or self.get_session()
        obj = session.query(self._model).filter_by(id=id).one()
        for attr, new_value in kwargs.items():
            setattr(obj, attr, new_value)
        session.commit()
        session.close()
        return obj

    def delete(self, id, session=None):
        """Delete record from database."""
        session = session or self.get_session()
        obj = session.query(self._model).filter_by(id=id).one()
        session.delete(obj)
        session.commit()
        session.close()


class UserManager(Manager):

    @property
    def _model(self):
        return User

    def add_group(self, id, group, session=None):
        session = (
            session
            or self.get_session.object_session(group)
            or self.get_session())
        user = self.get_by_id(id)
        user = session.merge(user)
        group = session.merge(group)
        user.groups.append(group)
        session.add(user)
        session.add(group)
        session.commit()


class GroupManager(Manager):

    @property
    def _model(self):
        return Group

    def add_user(self, id, user, session=None):
        session = (
            session
            or self.get_session.object_session(user)
            or self.get_session())
        group = self.get_by_id(id)
        user = session.merge(user)
        group = session.merge(group)
        group.users.append(user)
        session.add(user)
        session.add(group)
        session.commit()


class RatingManager(Manager):

    @property
    def _model(self):
        return Rating


class VenueManager(Manager):

    @property
    def _model(self):
        return Venue


class CategoryManager(Manager):

    @property
    def _model(self):
        return Category
