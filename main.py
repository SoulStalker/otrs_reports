import datetime
import calendar
import random

from analyzer import DataAnalyzer
from alcocheck import AlcoAnalyzer, beer_analyzer
from tg import TelegramBot
from settings import token, chat_id, alco_groups, ba_group, contacts


def get_message(analyzer, period):
    """
    Возвращает сообщение для телеги со смайликами
    :param analyzer:
    :param period:
    :return:
    """
    strongs = []
    poos = {}

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
    message = f'За {period} закрыли заявки: \n\n'
    for result in analyzer.results:
        agent = f' - {result[0]} {result[1]} - '
        tickets = result[2]
        message += agent
        message += str(tickets)
        if tickets >= 15 * multiplier:
            message += strong
            strongs.append(result[0])
        elif tickets >= 10 * multiplier:
            message += good
        elif tickets >= 5 * multiplier:
            message += little
        else:
            message += poo
            poos.setdefault(result[0], result[2])
    if len(poos) > 0:
        hero = min(poos.items(), key=lambda x: x[1])
        end_word = bad_work(hero[0])
    else:
        end_word = 'Надо же как отработали, ни одной какахи'
    if len(strongs) > 0:
        super_hero = max(strongs, key=lambda x: x[1])
        end_word = well_done(super_hero)
    return message, end_word


def alco_message(product):
    message = f'\U0001f943  У товара с кодом {product[0]} {product[1]} крепость {product[2]}. Группа {product[3]}'
    return message


def well_done(username):
    mess = [
            f"Спасибо, {username}, за то, что не дает нашим компьютерам помереть молча.",
            f"Наша поддержка похожа на чашку кофе - она всегда рядом и делает день лучше. Благодарим {username}!",
            f"{username} - как ниндзя в мире технической поддержки. Проблемы просто исчезают, когда он в деле!",
            f"С нашим {username} нет страха перед магическими словами '404' и 'ошибка сервера'!",
            f"{username} не нужны красные мантии - его костюм техподдержки смотрится лучше!",
            f"{username} наше решение для всех технических головоломок. На что бы мы делали без него?",
            f"Кто-то позвонил красной кнопке? А нет, это просто {username}, приходящий на помощь!",
            f"Похоже, {username} узнал секреты магии IT и щелкает пальцами, чтобы все работало!",
            ]
    return random.choice(mess)


def bad_work(username):
    mess = [
            f"{username} решил подарить нам неплохой драматический момент, играя 'Пропал в долгах с задачами'!",
            f"Мы слышали, что {username} начал отдыхать, потому что он закончил все задачи... в своих снах.",
            f"Мы организуем сбор средств для {username} - каждый, кто не отставал от плана, может скинуться на билет в будущее.",
            f"Считаем, что {username} взял на себя роль 'Двигатель экономии времени'. Мы ждем его производительных результатов!",
            f"Думаю, {username} решил устроить тайный мастер-класс 'Как увеличить количество невыполненных задач'.",
            f"Иногда {username} становится таким невидимым, что мы подозреваем, что он исследует науку камуфляжа.",
            f"Новое хобби {username}: не заниматься производительностью... ",
            f"Пока все мы учились решать задачи, {username} мастерил план 'Исчезновения из списка задач'.",
            f"Секрет успеха {username}: делать все медленнее, чем кажется возможным. Так, никто и не заметит!",
            f"Если {username} был бы профессиональным спящим, он был бы богат. Научитесь многому, наблюдая за ним!",
            f"Загадка {username}: почему он всегда такой медленный? Он, возможно, пытается победить в 'Медленном марафоне задач'!",
            f"Важно помнить, что {username} обратил задачу в искусство: искусство не заканчивать ничего.",
            f"Если {username} учился бы на факультете 'Отсрочки и оправдания', он был бы лучшим!",
            f"Мы подозреваем, что {username} работает по плану: 'Завалить всё, чтобы потом чудесно спасти'.",
            f"Секрет {username}: он считает, что лучшая задача - это задача, которую не нужно выполнять.",
            f"Кажется, {username} принял решение пойти на 'Отдыхательскую Олимпиаду' и выиграть золотую медаль в лежании на диване!",
            f"Пока все трудились, {username} исследовал феномен 'Исчезновение с рабочего места'.",
            f"Самый сложный вызов: попробовать понять, как {username} считает, что это нормально.",
            f"Если {username} учился бы в Школе Тормозологии, он был бы профессионалом!",
            f"Серьезное исследование: как {username} умудряется сделать меньше, чем ничего.",
            f"Мы думали, {username} - глава 'Клуба последнего минутчика'. Оказалось, он - единственный член!",
            f"Подсказка для {username}: чтобы сделать что-то, нужно начать сделывать что-то. Попробуйте!",
        ]
    return random.choice(mess)


def main():
    analyzer = DataAnalyzer()
    analyzer.get_results()
    analyzer.get_total_open_tickets()

    alco_analyzer = AlcoAnalyzer('13')

    telegram_api = TelegramBot(token=token, chat_id=chat_id)

    message, finish = get_message(analyzer, 'сегодня')

    telegram_api.send_message(message)
    telegram_api.send_message(finish)

    message = f'Открытых заявок осталось: {analyzer.total_open[0][0]}\n\n'
    message += f'Самая старая заявка {analyzer.total_open[0][1]}'

    telegram_api.send_message(message)

    # если сегодня воскресенье
    if datetime.datetime.today().weekday() == 6:
        message, finish = get_message(analyzer, 'месяц')

        telegram_api.send_message(message)
        print(message)
        telegram_api.send_message(finish)

    # если сегодня последний день месяца
    today = datetime.date.today()
    is_last_day_of_month = today.day == calendar.monthrange(today.year, today.month)[1]
    if is_last_day_of_month:
        message, finish = get_message(analyzer, 'месяц')

        telegram_api.send_message(message)
        print(message)
        telegram_api.send_message(finish)

    # дальше идет проверка алкоголя
    for k, v in contacts.items():
        if k == 'it_band':
            # пропускаем группу техподдержка
            continue
        telegram_api = TelegramBot(token=token, chat_id=v)
        alco_analyzer = AlcoAnalyzer(alco_groups[0])
        alco_analyzer.get_final_results()
        bad_news = alco_analyzer.results
        try:
            if len(bad_news[0]) > 0:
                # telegram_api.send_message(f'\U0001f6f0\uFE0F   Пщщ, пщщ... Хьюстон, у нас проблема')
                for product in bad_news:
                    telegram_api.send_message(alco_message(product))
            another_news = beer_analyzer(alco_groups[1], ba_group)
            for beer in another_news:
                # telegram_api.send_message(beer)
                print(alco_message(beer))
        except Exception as err:
            print(err)


if __name__ == "__main__":
    main()
