import time
import telepot
from telepot.loop import MessageLoop
import requests

token = "1171061388:AAFxZjpuP_3R9iQNZnnN6s74O5ottQcItFs"

bot = telepot.Bot(token)


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    message_id = msg["message_id"]
    first_name = msg["from"]["first_name"]
    if content_type == 'text':
        text = msg["text"]
        r = requests.post(url='http://faazi.ir/api/ask', data={'text': text})
        print(r)
        print(r.json())
        bot.sendMessage(chat_id, "Hello!")
    return


def on_callback_query(self, msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    message_id = msg['message']['message_id']
    chat_id = msg['from']['id']
    return


MessageLoop(bot, {'chat': handle,
                  'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
