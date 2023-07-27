from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Ticket(Base):
    __tablename__ = 'ticket'

    id = Column(Integer, primary_key=True)
    tn = Column(Integer)
    change_time = Column(DateTime)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)


class State(Base):
    __tablename__ = 'ticket_state'

    id = Column(Integer, primary_key=True)


class Queue(Base):
    __tablename__ = 'queue'

    id = Column(Integer, primary_key=True)
