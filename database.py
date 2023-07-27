from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import settings


def create_session(db_url):
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    return Session(), engine


dsn = settings.DSN
db, db_engine = create_session(dsn)