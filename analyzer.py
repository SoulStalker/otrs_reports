from datetime import timedelta, datetime
from sqlalchemy import Column, Integer, String, Date, func, select, text, cast

from database import db
from models import Ticket, User, Queue, State


class DataAnalyzer:

    def __init__(self):
        self.results = None
        self.total_open = None
        # self.month_results = None

    def get_results(self):
        with db as session:
            self.results = session.query(User.first_name,
                                         User.last_name,
                                         func.count(Ticket.tn).label('count')). \
                join(Ticket, User.id == Ticket.change_by). \
                filter(
                Ticket.ticket_state_id.in_([2]),
                text("CAST(Ticket.change_time AS DATE) = CURRENT_DATE"),
                Ticket.queue_id.in_([1, 4]),
                Ticket.change_by.notin_([6, 12])
            ). \
                group_by(User.first_name, User.last_name). \
                order_by(text('count DESC')). \
                limit(100). \
                all()

    def get_total_open_tickets(self):
        with db as session:
            self.total_open = session.query(func.count(Ticket.tn),
                                            func.min(cast(Ticket.change_time, Date))). \
                filter(
                Ticket.ticket_state_id == 1,
                Ticket.queue_id.in_([1, 4])
            ).limit(500).all()

    def get_month_results(self):
        with db as session:
            start_month = datetime(datetime.now().year, datetime.now().month, 1)
            end_month = datetime(datetime.now().year, datetime.now().month + 1, 1)

            self.results = session.query(User.first_name,
                                         User.last_name,
                                         func.count(Ticket.tn).label('count')). \
                join(Ticket, User.id == Ticket.change_by). \
                filter(
                Ticket.ticket_state_id.in_([2]),
                Ticket.change_time >= start_month,
                Ticket.change_time < end_month,
                Ticket.queue_id.in_([1, 4]),
                Ticket.change_by.notin_([6, 12])
            ). \
                group_by(User.first_name, User.last_name). \
                order_by(text('count DESC')). \
                limit(5000). \
                all()


def main():
    """
    Запуск анализа для проверки. Основной запуск из main.py
    :return:
    """
    analyzer = DataAnalyzer()
    analyzer.get_results()
    print(*analyzer.results)
    analyzer.get_total_open_tickets()
    print(*analyzer.total_open)
    analyzer.get_month_results()
    print(*analyzer.results)


if __name__ == '__main__':
    main()
