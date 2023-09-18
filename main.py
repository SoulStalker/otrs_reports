import datetime
import calendar

from analyzer import DataAnalyzer
from alcocheck import AlcoAnalyzer, beer_analyzer
from tg import TelegramBot
from settings import token, chat_id, alco_groups, ba_group, contacts


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


def alco_message(product):
    message = f'\U0001f943  У товара с кодом {product[0]} {product[1]} крепость {product[2]}. Группа {product[3]}'
    return message


def main():
    analyzer = DataAnalyzer()
    analyzer.get_results()
    analyzer.get_total_open_tickets()

    alco_analyzer = AlcoAnalyzer('13')

    telegram_api = TelegramBot(token=token, chat_id=chat_id)

    message = get_message(analyzer, 'сегодня')

    telegram_api.send_message(message)

    message = f'Открытых заявок осталось: {analyzer.total_open[0][0]}\n'
    message += f'Самая старая заявка {analyzer.total_open[0][1]}'

    telegram_api.send_message(message)

    # если сегодня воскресенье
    if datetime.datetime.today().weekday() == 6:
        message = get_message(analyzer, 'месяц')

        print(message)
        telegram_api.send_message(message)

    # если сегодня последний день месяца
    today = datetime.date.today()
    is_last_day_of_month = today.day == calendar.monthrange(today.year, today.month)[1]
    if is_last_day_of_month:
        message = get_message(analyzer, 'месяц')

        print(message)
        telegram_api.send_message(message)

    # дальше идет проверка алкоголя
    for k, v in contacts.items():
        if k == 'it_band':
            # пропускаем группу техподдержка
            continue
        telegram_api = TelegramBot(token=token, chat_id=v)
        alco_analyzer = AlcoAnalyzer(alco_groups[0])
        alco_analyzer.get_final_results()
        bad_news = alco_analyzer.results
        if len(bad_news[0]) > 0:
            # telegram_api.send_message(f'\U0001f6f0\uFE0F   Пщщ, пщщ... Хьюстон, у нас проблема')
            for product in bad_news:
                telegram_api.send_message(alco_message(product))
        another_news = beer_analyzer(alco_groups[1], ba_group)
        for beer in another_news:
            # telegram_api.send_message(beer)
            print(alco_message(beer))


if __name__ == "__main__":
    main()
