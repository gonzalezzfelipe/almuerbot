import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

user = os.environ['MYSQL_USER']
password = os.environ['MYSQL_PASSWORD']
db = os.environ['MYSQL_DATABASE']

if os.environ['ALMUERBOT_TEST']:
    engine = create_engine('sqlite:///test.db')
else:
    engine = create_engine(
        'mysql+pymysql://{}:{}@localhost:3306/{}'.format(user, password, db))
Session = sessionmaker(bind=engine)

Base = declarative_base()
