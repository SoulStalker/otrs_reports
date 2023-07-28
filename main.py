import datetime

from analyzer import DataAnalyzer
from tg import TelegramBot
from settings import token, chat_id


def get_message(analyzer, period):
    strong = f'   \U0001F4AA\n'
    good = f'   \U0001F44D\n'
    little = f'   \U0001F90F\n'
    poo = f'   \U0001F4A9\n'
    if period == 'сегодня':
        multiplier = 1
        analyzer.get_results()
    elif period == 'месяц':
        multiplier = 10
        analyzer.get_month_results()
    message = f'За {period} закрыли заявки: \n'
    for result in analyzer.results:
        agent = f'{result[0]} {result[1]} - '
        tickets = result[2]
        message += agent
        message += str(tickets)
        if tickets >= 15 * multiplier:
            message += strong
        elif tickets >= 10 * multiplier:
            message += good
        elif tickets >= 5 * multiplier:
            message += little
        else:
            message += poo

    return message


def main():
    analyzer = DataAnalyzer()
    analyzer.get_results()
    analyzer.get_total_open_tickets()
    telegram_api = TelegramBot(token=token, chat_id=chat_id)

    message = get_message(analyzer, 'сегодня')

    print(message)
    telegram_api.send_message(message)

    message = f'Открытых заявок осталось: {analyzer.total_open[0][0]}\n'
    message += f'Самая старая заявка {analyzer.total_open[0][1]}'

    telegram_api.send_message(message)

    if datetime.datetime.today().weekday() == 4:
        message = get_message(analyzer, 'месяц')

        print(message)
        telegram_api.send_message(message)


if __name__ == "__main__":
    main()
