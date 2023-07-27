from datetime import timedelta, datetime
from sqlalchemy import Column, Integer, String, Date, func, select, text

from database import db
from models import Ticket, User, Queue, State


class DataAnalyzer:

    def __init__(self):
        self.results = None

    def get_results(self):
        with db as session:
            self.results = session.query(User.first_name,
                                         User.last_name,
                                         func.count(Ticket.tn).label('count')). \
                join(Ticket, User.id == Ticket.change_by). \
                filter(
                Ticket.ticket_state_id.in_([2, 3]),
                text("CAST(Ticket.change_time AS DATE) = CURRENT_DATE"),
                Ticket.queue_id.in_([1, 4]),
                Ticket.change_by.notin_([6, 12])
            ). \
                group_by(User.first_name, User.last_name). \
                order_by(text('count DESC')). \
                limit(100). \
                all()


def main():
    """
    Запуск анализа для проверки. Основной запуск из main.py
    :return:
    """
    analyzer = DataAnalyzer()
    analyzer.get_results()
    print(*analyzer.results)


if __name__ == '__main__':
    main()
