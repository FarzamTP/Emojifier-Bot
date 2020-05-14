import time
import telepot
from telepot.loop import MessageLoop
import requests
import emoji
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup

token = "1171061388:AAFxZjpuP_3R9iQNZnnN6s74O5ottQcItFs"

bot = telepot.Bot(token)


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        text = msg["text"]
        if text == '/start':
            bot.sendMessage(chat_id, "Hello!\nI am Emojizer, a newly born sense detector robot!\nI am in my primary "
                                     "stages of learning, so it may take a little time for me to respond...\nAs a "
                                     "child, I can not memorize long sentences (more than 10 words), complex words "
                                     "and also punctioation marks...\nPlease don't use them...\n")
            bot.sendMessage(chat_id, "Now, Tell what you think...")
        else:
            bot.sendMessage(chat_id, "Processing your text...")
            r = requests.post(url='https://faazi.ir/api/ask', data={'text': text})
            emoji_unicode = r.json().get('emoji')
            prob = float(r.json().get('prob'))
            keyboard = like_dislike_keyboard()
            bot.sendMessage(chat_id, emoji.emojize(text + " %s with probability %.3f" % (emoji_unicode, prob),
                                                   use_aliases=True), reply_markup=keyboard)

    return


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    message_id = msg['message']['message_id']
    chat_id = msg['from']['id']

    msg_identifier = (chat_id, message_id)
    bot.editMessageReplyMarkup(msg_identifier)

    if str(query_data) == "like":
        bot.sendMessage(chat_id, emoji.emojize("Yeah :tada: Thanks for your support. :smile:", use_aliases=True))
        bot.sendMessage(chat_id, "Tell me more...")
    elif str(query_data) == "dislike":
        bot.sendMessage(chat_id, "Sorry that I couldn't understand you :sad:\nI'll grow better with help of nice guys "
                                 "like you :heart_eyes:")
        bot.sendMessage(chat_id, "Tell me more...")


def like_dislike_keyboard():
    keyboard = [
        [InlineKeyboardButton(text=emoji.emojize(":thumbsup:", use_aliases=True), callback_data="like"),
         InlineKeyboardButton(text=emoji.emojize(":thumbsdown:", use_aliases=True), callback_data="dislike")],
    ]
    main_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return main_keyboard


MessageLoop(bot, {'chat': handle,
                  'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
