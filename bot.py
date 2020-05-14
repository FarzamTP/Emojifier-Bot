import time
import telepot
from telepot.loop import MessageLoop
import requests
import emoji
import string
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime

me = 313030525
mutex = False
token = "1171061388:AAFxZjpuP_3R9iQNZnnN6s74O5ottQcItFs"

bot = telepot.Bot(token)


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        text = msg["text"]
        if text == '/start':
            bot.sendMessage(chat_id,
                            "Hello!\nI am Emojizer, a newly born sense detector robot!\nI am in my primary "
                            "stages of learning, so it may take a little time for me to respond...\nAs a "
                            "child, I can not memorize long sentences (more than 10 words), complex words "
                            "and also punctioation marks...\nPlease don't use them...\n")
            bot.sendMessage(chat_id, "Now, Tell what you think...")
        else:
            global mutex
            if not mutex:
                if less_than_ten_words(text):
                    if not contains_punc(text):
                        inform_me("User %s sent: %s" % (str(chat_id), str(text)))
                        mutex = True
                        t1 = datetime.now()

                        bot.sendMessage(chat_id, "Processing your text...")
                        r = requests.post(url='https://faazi.ir/api/ask', data={'text': text})
                        emoji_unicode = r.json().get('emoji')
                        prob = float(r.json().get('prob'))
                        keyboard = like_dislike_keyboard()

                        spent_time = (datetime.now() - t1).total_seconds()
                        bot.sendMessage(chat_id, emoji.emojize(
                                "Took %d seconds to process...\n" % spent_time + text + " %s with probability %.3f" % (
                                    emoji_unicode, prob), use_aliases=True), reply_markup=keyboard)

                        bot.sendMessage(me, emoji.emojize(
                                "Took %d seconds to process...\n" % spent_time + text + " %s with probability %.3f" % (
                                    emoji_unicode, prob), use_aliases=True), reply_markup=keyboard)
                        mutex = False
                    else:
                        bot.sendMessage(chat_id, "Please don't enter punctuation marks...")
                        bot.sendMessage(chat_id, "Now, Tell what you think...")
                else:
                    bot.sendMessage(chat_id, "Please enter shorter sentence...\nless than 10 words...")
            else:
                bot.sendMessage(chat_id, "I'm processing right now.. \nPlease try again in a few minutes.")
    return


def inform_me(text):
    bot.sendMessage(me, text)


def less_than_ten_words(text):
    if len(str(text).split(" ")) < 10:
        return True
    else:
        return False


def contains_punc(text):
    flag = False
    for p in string.punctuation:
        if p in text:
            flag = True
            break
    return flag


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    message_id = msg['message']['message_id']
    chat_id = msg['from']['id']

    msg_identifier = (chat_id, message_id)
    bot.editMessageReplyMarkup(msg_identifier)

    if str(query_data) == "like":
        bot.sendMessage(chat_id, emoji.emojize("Yeah :tada: Thanks for your support. :smile:", use_aliases=True))
        bot.sendMessage(me, emoji.emojize("Yeah :tada: Thanks for your support. :smile:", use_aliases=True))

        bot.sendMessage(chat_id, "Tell me more...")
    elif str(query_data) == "dislike":
        bot.sendMessage(chat_id, emoji.emojize("Sorry that I couldn't understand you :pensive:\nI'll grow better with "
                                               "help of nice guys like you :heart_eyes:", use_aliases=True))
        bot.sendMessage(me, emoji.emojize("Sorry that I couldn't understand you :pensive:\nI'll grow better with "
                                          "help of nice guys like you :heart_eyes:", use_aliases=True))
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
