from sqlalchemy import Column, String, Integer, Date

from base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    email = Column(String)

    def __init__(self, name, username, email):
        self.name = name
        self.username = username
        self.email = email

    def __as_dict__(self):
        return {
            'id': self.id
            'name': self.name,
            'username': self.username,
            'email': self.email}
