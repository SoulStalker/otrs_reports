import requests


class TelegramBot:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id

    def send_message(self, text):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        ftext = f'''
        <code>{text}</code>
        '''
        params = {"chat_id": self.chat_id, "text": ftext, "parse_mode": "HTML"}
        response = requests.post(url, data=params)
        return response.json()
