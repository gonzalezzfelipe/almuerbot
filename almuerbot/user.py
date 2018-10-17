from sqlalchemy import Column, String, Integer, Date

from base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    slack = Column(String)

    def __init__(self, name, email, slack):
        self.name = name
        self.email = email
        self.slack = slack
