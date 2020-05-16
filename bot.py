import time
import telepot
from telepot.loop import MessageLoop
import requests
import emoji
import string
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime

me = 313030525
channel_id = -1001499881955
mutex = False
token = "1171061388:AAFxZjpuP_3R9iQNZnnN6s74O5ottQcItFs"
URL = 'https://faraanak.ir/'
bot = telepot.Bot(token)


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        text = msg["text"]
        global mutex
        if text == '/start':
            bot.sendMessage(chat_id,
                            "Hello!\nI am Emojizer, a newly born sense detector robot!\nI am in my primary "
                            "stages of learning, so it may take a little time for me to respond...\nAs a "
                            "child, I can not memorize long sentences (more than 10 words), complex words "
                            "and also punctuation marks...\nPlease don't use them...\n"
                            "If I didn't start processing immediately: \n\n----> PLEASE DO‌ NOT HESITATE!!! <----\n\n"
                            "That's because I'm processing at the moment and will process your sentence in a minute.‌")
            bot.sendMessage(chat_id, "Now, Tell what you think...")
        elif text == '/label_sentence':
            bot.sendMessage(channel_id, "[Profile](tg://user?id=%s) asked to label unassigned sentences..." %
                            str(chat_id), parse_mode="Markdown")

            r = requests.get(url=URL + 'api/load_unassigned')
            print(r.ok)
            if r.ok:
                status = r.json().get('status')
                if status == 200:
                    bot.sendMessage(chat_id, "Loading sentence...")

                    sentence_id = str(r.json().get('id'))
                    text = str(r.json().get('text'))
                    predicted_emoji = str(r.json().get('predicted_emoji'))
                    prob = float(r.json().get('prob'))

                    keyboard = like_dislike_keyboard(sentence_id, predicted_emoji)

                    bot.sendMessage(chat_id, emoji.emojize(text + " %s with probability %.3f" % (predicted_emoji, prob),
                                                           use_aliases=True), reply_markup=keyboard)

                    bot.sendMessage(channel_id, emoji.emojize(text + " %s with probability %.3f" % (predicted_emoji, prob),
                                                              use_aliases=True))
                elif status == 201:
                    bot.sendMessage(chat_id, "No more sentences for labeling!\nThanks for your support.")
        else:
            if not mutex:
                if less_than_ten_words(text):
                    if not contains_punc(text):
                        if str(text).lower() == 'export to csv' and str(chat_id) == str(me):
                            mutex = True
                            bot.sendMessage(chat_id, "Started to export...")
                            r = requests.get(url=URL + 'api/export')
                            if r.ok:
                                with open('./media/data.csv', 'r') as file:
                                    bot.sendDocument(me, file, 'Exported data')
                            mutex = False
                        else:
                            predict_sentence(chat_id, text)
                    else:
                        text = text.translate(str.maketrans('', '', string.punctuation))
                        predict_sentence(chat_id, text)
                        # bot.sendMessage(chat_id, "Please don't enter punctuation marks...")
                        # bot.sendMessage(chat_id, "Now, Tell what you think...")
                else:
                    bot.sendMessage(chat_id, "Please enter shorter sentence...\nless than 10 words...")
            else:
                bot.sendMessage(chat_id, "I'm processing right now.. \nPlease try again in a few minutes.")
    return


def predict_sentence(chat_id, text):
    bot.sendMessage(channel_id,
                    text="[Profile](tg://user?id=%s) sent '%s'" % (str(chat_id), text),
                    parse_mode="Markdown")
    global mutex
    mutex = True
    t1 = datetime.now()

    bot.sendMessage(chat_id, "Processing your text...")
    r = requests.post(url=URL + 'api/ask', data={'text': text})
    if r.ok:
        emoji_unicode = r.json().get('emoji')
        prob = float(r.json().get('prob'))
        sentence_id = str(r.json().get('sentence_id'))
        keyboard = like_dislike_keyboard(sentence_id, emoji_unicode)

        spent_time = (datetime.now() - t1).total_seconds()
        bot.sendMessage(chat_id, emoji.emojize(
            "Took %d seconds to process...\n" % spent_time + text + " %s with probability %.3f" % (
                emoji_unicode, prob), use_aliases=True), reply_markup=keyboard)

        bot.sendMessage(channel_id, emoji.emojize(
            "Took %d seconds to process...\n" % spent_time + text + " %s with probability %.3f" % (
                emoji_unicode, prob), use_aliases=True))
    else:
        bot.sendMessage(chat_id, emoji.emojize("I couldn't understand the words... :pensive:",
                                               use_aliases=True))
    mutex = False


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

    if len(str(query_data).split(" ")) == 3:
        action = str(query_data).split(" ")[0]
        sentence_id = str(query_data).split(" ")[1]
        emoji_unicode = str(query_data).split(" ")[2]

        if action == "like":
            bot.sendMessage(chat_id, emoji.emojize("Yeah :tada: Thanks for your support. :smile:", use_aliases=True))

            # Posts to channel
            bot.sendMessage(channel_id, emoji.emojize("Yeah :tada: Thanks for your support. :smile:", use_aliases=True))
            submit_impression(action, sentence_id, emoji_unicode)
            bot.sendMessage(chat_id, "Tell me more...")
        elif action == "dislike":
            new_keyboard = other_emoji_keyboard(emoji_unicode, sentence_id)
            bot.sendMessage(chat_id, emoji.emojize("Sorry that I couldn't understand you :pensive:\nI'll grow better "
                                                   "with help of nice guys like you :heart_eyes:\nPlease choose the "
                                                   "correct emoji",
                                                   use_aliases=True), reply_markup=new_keyboard)

        elif action == 'label':
            bot.sendMessage(channel_id,
                            emoji.emojize("[Profile](tg://user?id=%s) submitted %s" % (str(chat_id), emoji_unicode),
                                          use_aliases=True),
                            parse_mode="Markdown")
            status = submit_impression(action, sentence_id, emoji_unicode)
            if status == 200:
                bot.sendMessage(chat_id, "Thanks for your help!")
            bot.sendMessage(chat_id, "Tell me more...")


def submit_impression(action, sentence_id, emoji_unicode):
    r = requests.post(url=URL + 'api/submit', data={'action': action, 'sentence_id': sentence_id,
                                                    'emoji_unicode': emoji_unicode})
    status = r.json().get('status')
    return status


def other_emoji_keyboard(emoji_unicode, sentence_id):
    keyboard = [[], []]

    emoji_unicode_list = [':heart:', ':heart_eyes:', ':smile:', ':disappointed:', ':expressionless:',
                          ':see_no_evil:', ':neutral_face:', ':scream:', ':rage:', ':fork_and_knife:', ':baseball:']
    emoji_unicode_list.remove(emoji_unicode)

    for idx, emoji_code in enumerate(emoji_unicode_list):
        keyboard[int(idx / 5)].append(
            InlineKeyboardButton(text=emoji.emojize(emoji_code, use_aliases=True),
                                 callback_data="label %s %s" % (str(sentence_id), emoji_code))
        )

    main_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return main_keyboard


def like_dislike_keyboard(sentence_id, emoji_unicode):
    keyboard = [
        [InlineKeyboardButton(text=emoji.emojize(":thumbsup:", use_aliases=True),
                              callback_data="like " + sentence_id + " " + str(emoji_unicode)),
         InlineKeyboardButton(text=emoji.emojize(":thumbsdown:", use_aliases=True),
                              callback_data="dislike " + sentence_id + " " + str(emoji_unicode))],
    ]
    main_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return main_keyboard


MessageLoop(bot, {'chat': handle,
                  'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
