import datetime

from analyzer import DataAnalyzer
from tg import TelegramBot
from settings import token, chat_id


def main():
    analyzer = DataAnalyzer()
    analyzer.get_results()
    analyzer.get_total_open_tickets()
    telegram_api = TelegramBot(token=token, chat_id=chat_id)

    message = f'За сегодня закрыли заявки: \n'
    for result in analyzer.results:
        agent = f'{result[0]} {result[1]} - '
        tickets = result[2]
        message += agent
        message += str(tickets)
        if tickets > 14:
            message += f'   \U0001F4AA\n'
        elif tickets > 9:
            message += f'   \U0001F44D\n'
        elif tickets > 4:
            message += f'   \U0001F90F\n'
        else:
            message += f'   \U0001F4A9\n'

    print(message)
    telegram_api.send_message(message)

    message = f'Открытых заявок осталось: {analyzer.total_open[0][0]}\n'
    message += f'Самая старая заявка {analyzer.total_open[0][1]}'

    telegram_api.send_message(message)

    if datetime.datetime.today().weekday() == 6:
        message = f'С начала месяца закрыли заявки: \n'
        analyzer.get_month_results()
        for month_result in analyzer.month_results:
            agent = f'{month_result[0]} {month_result[1]} - '
            tickets = month_result[2]
            message += agent
            message += str(tickets)
            if tickets > 150:
                message += f'   \U0001F4AA\n'
            elif tickets > 100:
                message += f'   \U0001F44D\n'
            elif tickets > 50:
                message += f'   \U0001F90F\n'
            else:
                message += f'   \U0001F4A9\n'

        print(message)
        telegram_api.send_message(message)


if __name__ == "__main__":
    main()
