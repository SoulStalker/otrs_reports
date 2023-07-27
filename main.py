from analyzer import DataAnalyzer
from tg import TelegramBot
from settings import token, chat_id


def main():
    analyzer = DataAnalyzer()
    analyzer.get_results()
    telegram_api = TelegramBot(token=token, chat_id=chat_id)

    message = f'За сегодня закрыли заявки: \n'
    for result in analyzer.results:
        agent = f'{result[0]} {result[1]} - '
        tickets = result[2]
        message += agent
        message += str(tickets)
        if tickets > 14:
            message += f' \U0001F4AA\n'
        elif tickets > 9:
            message += f' \U0001F44D\n'
        elif tickets > 4:
            message += f' \U0001F90F\n'
        else:
            message += f' \U0001F4A9\n'


    print(message)
    # telegram_api.send_message(message)


if __name__ == "__main__":
    main()
