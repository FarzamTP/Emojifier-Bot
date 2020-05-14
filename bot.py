import time
import telepot
from telepot.loop import MessageLoop
import requests
import emoji


token = "1171061388:AAFxZjpuP_3R9iQNZnnN6s74O5ottQcItFs"

bot = telepot.Bot(token)


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        text = msg["text"]
        if text == '/start':
            bot.sendMessage(chat_id, "Hello!\nI am Emojizer, a newly born sense detector robot!\nI am in my primary "
                                     "stages of learning so it may take a little time for me to response...\nAs a "
                                     "child, I can not memorize long sentences, complex words and also punctioation "
                                     "marks...\nTell what you think...")
        else:
            bot.sendMessage(chat_id, "Processing your text...")
            r = requests.post(url='https://faazi.ir/api/ask', data={'text': text})
            emoji_unicode = r.json().get('emoji')
            prob = float(r.json().get('prob'))
            bot.sendMessage(chat_id, emoji.emojize(text + " %s with probability %.3f" % (emoji_unicode, prob),
                                                   use_aliases=True))
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
