# coding=utf-8
import telebot
from telebot import types
import os
from flask import Flask, request
import logging
import time
from db import search_scene
from select_loc import select_loc

# bot key
bot = telebot.TeleBot('354356282:AAFxIjCrjJMn0qeoiNKFQnBTKNr8yDl0giY')
telebot.logger.setLevel(logging.DEBUG)
server = Flask(__name__)

# start command


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)
    bot.send_message(message.from_user.id,
                     u'您好，我是旅行助手BOT\n功能解說\n/search 可以搜尋附近的旅遊景點~\n@GoGoTest_Bot 可以啟用助手的搜尋功能，可以在任何對話框搜尋景點，並分享給好友\n/help 查看BOT使用指南')

# search scenes command


@bot.message_handler(commands=['search'])
def deal_message(message):
    print message
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn = types.KeyboardButton(u'傳送座標', request_location=True)
    markup.add(itembtn)
    bot.send_message(message.from_user.id,
                     u'請輸入你的地點，您可以點選按鈕快速傳送個人位置\n或者打字輸入地名，例如輸入台南，即可找台南的旅遊景點', reply_markup=markup)

# help command


@bot.message_handler(commands=['help'])
def deal_help(message):
    bot.send_message(message.from_user.id,
                     u'/search 可以搜尋附近的旅遊景點~\n@GoGoTest_Bot 可以啟用助手的搜尋功能，可以在任何對話框搜尋景點，並分享給好友')

# deal with text, bot will search the target location


@bot.message_handler(func=lambda message: True, content_types=['text'])
def deal_text(message):
    print message
    select_loc(message.text, message.from_user.id, 1)

# deal with location, bot will search the scene around the user


@bot.message_handler(func=lambda location: True, content_types=['location'])
def deal_location(message):
    px = message.location.longitude
    py = message.location.latitude
    print px
    print py
    search_scene(message.from_user.id, px, py, 0, 0, 0)

# deal with want to watch more and google map


@bot.callback_query_handler(func=lambda call: True)
def test_callback(call):
    print call
    if u'wanttowatch2' in call.data:
        count2 = int(call.data.split()[1])
        tag = float(call.data.split()[2])
        search_scene(call.from_user.id, 0, 0, count2, 1, tag)
    elif(u"wanttowatch" in call.data):
        count2 = int(call.data.split()[1])
        px = float(call.data.split()[2])
        py = float(call.data.split()[3])
        search_scene(call.from_user.id, px, py, count2, 0, 0)
    else:
        px = call.data.split()[0]
        py = call.data.split()[1]
        bot.send_location(call.from_user.id, py, px)

# inline command


@bot.inline_handler(lambda query: True)
def query_photo(inline_query):
    print inline_query
    try:
        # first, bot will show the scene around the user
        if inline_query.query == '':
            px = inline_query.location.longitude
            py = inline_query.location.latitude
            answer = search_scene(inline_query.id, px, py, 0, 2, 0)
            bot.answer_inline_query(inline_query.id, answer, cache_time=1)
         # if user input somthing, bot will search the scene in target
        else:
            text = inline_query.query
            answer = select_loc(text, inline_query.id, 3)
            bot.answer_inline_query(inline_query.id, answer, cache_time=1)
    except Exception as e:
        print(e)


@server.route("/", methods=['POST'])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://gogotestvicharm.herokuapp.com/")
    return "!", 200


server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
server = Flask(__name__)
bot.polling(True)
while 1:
    time.sleep(3)
