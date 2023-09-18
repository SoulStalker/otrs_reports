from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import settings


def create_session(db_url):
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    return Session(), engine


dsn = settings.DSN
dsn_set = settings.DSN_SET
db, db_engine = create_session(dsn)
db_set, set_engine = create_session(dsn_set)


