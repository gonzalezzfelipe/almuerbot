from sqlalchemy import Column, String, Integer, Date

from almuerbot.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    username = Column(String(50))
    email = Column(String(50))

    def __init__(self, name, username, email):
        self.name = name
        self.username = username
        self.email = email

    def __as_dict__(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'email': self.email}
