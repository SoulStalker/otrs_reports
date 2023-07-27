from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)


class State(Base):
    __tablename__ = 'ticket_state'

    id = Column(Integer, primary_key=True)


class Queue(Base):
    __tablename__ = 'queue'

    id = Column(Integer, primary_key=True)


class Ticket(Base):
    __tablename__ = 'ticket'

    id = Column(Integer, primary_key=True)
    tn = Column(Integer)
    change_time = Column(DateTime)
    change_by = Column(Integer, ForeignKey('users.id'))
    ticket_state_id = Column(Integer, ForeignKey('ticket_state.id'))
    queue_id = Column(Integer, ForeignKey('queue.id'))



