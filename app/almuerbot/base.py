import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

user = os.environ.get('MYSQL_USER', 'almuerbot')
password = os.environ.get('MYSQL_PASSWORD', 'almuerbot')
db = os.environ.get('MYSQL_DATABASE', 'almuerbot')

if os.environ.get('ALMUERBOT_TEST', False):
    engine = create_engine('sqlite:///test.db')
else:
    engine = create_engine(
        'mysql+pymysql://{}:{}@db:3306/almuerbot'.format(user, password, db))
Session = sessionmaker(bind=engine)

Base = declarative_base()
