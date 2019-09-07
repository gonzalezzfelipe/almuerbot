import logging
from abc import ABC, abstractproperty

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from almuerbot.config import constants
from almuerbot.data.models import Rating, User, Venue


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
        conditions = []
        for attr_name, value in filters.items():
            if isinstance(value, list):
                conditions.append(getattr(self._model, attr_name).in_(value))
            if isinstance(value, tuple):
                conditions.append(
                    getattr(self._model, attr_name).between(*value))
            else:
                conditions.append(getattr(self._model, attr_name) == value)
        session = self.get_session()
        ret_values = session.query(self._model).filter(*conditions)
        session.close()
        return ret_values

    def get_first(self, **filters):
        """Get first matching value."""
        try:
            return self.get(**filters)[0]
        except IndexError:
            return None

    def add(self, *args, **kwargs):
        """Add to database."""
        obj = self._model(*args, **kwargs)
        session = self.get_session()
        session.add(obj)
        ret_val = obj.as_dict()
        session.commit()
        session.close()
        return ret_val

    def update(self, id, **kwargs):
        """Update row by id."""
        session = self.get_session()
        obj = session.query(self._model).filter_by(id=id).one()
        for attr, new_value in kwargs.items():
            setattr(obj, attr, new_value)
        ret_val = obj.as_dict()
        session.commit()
        session.close()
        return ret_val

    def delete(self, id):
        """Delete record from database."""
        session = self.get_session()
        obj = session.query(self._model).filter_by(id=id).one()
        session.delete(obj)
        session.commit()
        session.close()


class UserManager(Manager):
    @property
    def _model(self):
        return User


class RatingManager(Manager):
    @property
    def _model(self):
        return Rating


class VenueManager(Manager):
    @property
    def _model(self):
        return Venue
