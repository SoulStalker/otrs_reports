from analyzer import DataAnalyzer
from tg import TelegramBot
from settings import token, chat_id


def main():
    analyzer = DataAnalyzer()
    analyzer.get_results()
    telegram_api = TelegramBot(token=token, chat_id=chat_id)

    message = f'За сегодня закрыли заявки: \n'
    for result in analyzer.results:
        message += f'{result[0]} {result[1]}  - {result[2]}\n'

    print(message)
    telegram_api.send_message(message)


if __name__ == "__main__":
    main()
