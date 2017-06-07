# -*- coding: utf-8 -*-
"""
Created on Sat May 06 17:09:05 2017

@author: vicharm
"""

# -*- coding:utf-8 -*-
import pymongo
import telebot
from telebot import types
import logging


# Standard URI format: mongodb://[dbuser:dbpassword@]host:port/dbname
uri = 'mongodb://vic010744:vic32823@ds147711.mlab.com:47711/heroku_jvwg4955'
###############################################################################
# main
###############################################################################
bot = telebot.TeleBot('354356282:AAFxIjCrjJMn0qeoiNKFQnBTKNr8yDl0giY')
telebot.logger.setLevel(logging.DEBUG)

# mode=0 為鄰近位置景點搜尋
# mode=1 為指定縣市搜尋 tag代表不同縣市
# mode=2 為inline鄰近位置搜尋
# mode=3 為inline指定縣市搜尋 tag代表不同縣市
# count2 is the number of scenes had watched by user


def search_scene(sender_id, px, py, count2, mode, tag):
    print 'in search_scene'
    # db initial
    client = pymongo.MongoClient(uri)
    db = client.get_default_database()
    scenes = db['travel']
    if(tag == 30):
        bot.send_message(message.from_user.id,
                     u'不好意思 目前只支援縣市搜尋')

    # initial number of scene
    count = 0
    if mode == 0:
        for doc in scenes.find():
            # compute the distance <= 0.015 on google map
            if(pow(float(doc['Px']) - px, 2) + pow(float(doc['Py']) - py, 2) < 0.015):
                print "in find"

                # user had not saw these scenes
                if count >= count2:
                    # 4 new scenes, and send want watch more
                    if(count >= count2 + 4):
                        markup = types.InlineKeyboardMarkup()
                        itembtn = types.InlineKeyboardButton(
                            u"想看更多", callback_data="wanttowatch {} {} {}".format(count, px, py))
                        markup.add(itembtn)
                        bot.send_message(sender_id, u"想看更多嗎?",
                                         reply_markup=markup)
                        break
                    # count < count2 + 4 , get information from db
                    else:
                        print doc['_id']
                        name = doc['Name']
                        discription = doc['Toldescribe']
                        lan = doc['Px']
                        lat = doc['Py']
                        text = "<a href=" + "\"" + \
                            doc['Picture1'] + "\">" + name + "</a>"
                        bot.send_message(sender_id, text=text,
                                         parse_mode="HTML")
                        markup = types.InlineKeyboardMarkup()
                        itembtn = types.InlineKeyboardButton(
                            u"導航帶我去", callback_data=str(lan) + ' ' + str(lat))
                        markup.add(itembtn)
                        bot.send_message(
                            sender_id, text=discription, reply_markup=markup)
                count = count + 1
        if(count == 0):
            bot.send_message(sender_id, "嗚嗚嗚不好意思，找不到相對應的結果")
    elif mode == 2:
        # search suitable data and stor in answer list
        answer = []
        for doc in scenes.find():
            if(pow(float(doc['Px']) - px, 2) + pow(float(doc['Py']) - py, 2) < 0.015):
                # use doc_parse function to get information and merge answer
                answer = doc_parse(doc, answer, count)
                count = count + 1
                # 25 is api upperbound
                if count == 24:
                    return answer
        return answer
    # mode = 1 or 3
    else:
        end = 0
        if mode == 3:
            answer = []
        if tag == 0:   # tainan
            for doc in scenes.find():
                end = 0
                if u'tainan' in doc['Add'] or u'台南' in doc['Add'] or u'Tainan' in doc['Add']:
                    print "in find tainan"
                    if mode == 3:
                        answer = doc_parse(doc, answer, count)
                        if count == 24:
                            return answer

                    else:
                        if count >= count2:
                            # deal scene is function to get information and
                            # send scenes
                            end = deal_scene(
                                count, count2, tag, doc, sender_id)
                        if end == 1:
                            break
                    count = count + 1
            if(count == 0 and mode == 1):
                bot.send_message(sender_id, "嗚嗚嗚不好意思，找不到相對應的結果")
            elif mode == 3:
                return answer
        elif tag == 1:
            for doc in scenes.find():
                if u'臺北' in doc['Add']:
                    print "in find"
                    if mode == 3:
                        answer = doc_parse(doc, answer, count)
                        if count == 24:
                            return answer
                    else:
                        if count >= count2:
                            end = deal_scene(
                                count, count2, tag, doc, sender_id)
                        if end == 1:
                            break
                    count = count + 1
            if(count == 0 and mode == 1):
                bot.send_message(sender_id, "嗚嗚嗚不好意思，找不到相對應的結果")
            elif mode == 3:
                return answer
        elif tag == 2:
            for doc in scenes.find():
                if u'新北' in doc['Add']:
                    if mode == 3:
                        answer = doc_parse(doc, answer, count)
                        if count == 24:
                            return answer
                    else:
                        if count >= count2:
                            end = deal_scene(
                                count, count2, tag, doc, sender_id)
                        if end == 1:
                            break
                    count = count + 1
            if(count == 0 and mode == 1):
                bot.send_message(sender_id, "嗚嗚嗚不好意思，找不到相對應的結果")
            elif mode == 3:
                return answer
        elif tag == 3:
            for doc in scenes.find():
                if u'基隆' in doc['Add']:
                    if mode == 3:
                        answer = doc_parse(doc, answer, count)
                        if count == 24:
                            return answer
                    else:
                        if count >= count2:
                            end = deal_scene(
                                count, count2, tag, doc, sender_id)
                        if end == 1:
                            break
                    count = count + 1
            if(count == 0 and mode == 1):
                bot.send_message(sender_id, "嗚嗚嗚不好意思，找不到相對應的結果")
            elif mode == 3:
                return answer
        elif tag == 4:
            for doc in scenes.find():
                if u'桃園' in doc['Add']:
                    if mode == 3:
                        answer = doc_parse(doc, answer, count)
                        if count == 24:
                            return answer
                    else:
                        if count >= count2:
                            end = deal_scene(
                                count, count2, tag, doc, sender_id)
                        if end == 1:
                            break
                    count = count + 1
            if(count == 0 and mode == 1):
                bot.send_message(sender_id, "嗚嗚嗚不好意思，找不到相對應的結果")
            elif mode == 3:
                return answer
        elif tag == 5:
            for doc in scenes.find():
                if u'新竹' in doc['Add']:
                    if mode == 3:
                        answer = doc_parse(doc, answer, count)
                        if count == 24:
                            return answer
                    else:
                        if count >= count2:
                            end = deal_scene(
                                count, count2, tag, doc, sender_id)
                        if end == 1:
                            break
                    count = count + 1
            if(count == 0 and mode == 1):
                bot.send_message(sender_id, "嗚嗚嗚不好意思，找不到相對應的結果")
            elif mode == 3:
                return answer
        elif tag == 6:
            for doc in scenes.find():
                if u'苗栗' in doc['Add']:
                    if mode == 3:
                        answer = doc_parse(doc, answer, count)
                        if count == 24:
                            return answer
                    else:
                        if count >= count2:
                            end = deal_scene(
                                count, count2, tag, doc, sender_id)
                        if end == 1:
                            break
                    count = count + 1
            if(count == 0 and mode == 1):
                bot.send_message(sender_id, "嗚嗚嗚不好意思，找不到相對應的結果")
            elif mode == 3:
                return answer
        elif tag == 7:
            for doc in scenes.find():
                if u'台中' in doc['Add']:
                    if mode == 3:
                        answer = doc_parse(doc, answer, count)
                        if count == 24:
                            return answer
                    else:
                        if count >= count2:
                            end = deal_scene(
                                count, count2, tag, doc, sender_id)
                        if end == 1:
                            break
                    count = count + 1
            if(count == 0 and mode == 1):
                bot.send_message(sender_id, "嗚嗚嗚不好意思，找不到相對應的結果")
            elif mode == 3:
                return answer
        elif tag == 8:
            for doc in scenes.find():
                if u'彰化' in doc['Add']:
                    if mode == 3:
                        answer = doc_parse(doc, answer, count)
                        if count == 24:
                            return answer
                    else:
                        if count >= count2:
                            end = deal_scene(
                                count, count2, tag, doc, sender_id)
                        if end == 1:
                            break
                    count = count + 1
            if(count == 0 and mode == 1):
                bot.send_message(sender_id, "嗚嗚嗚不好意思，找不到相對應的結果")
            elif mode == 3:
                return answer
        elif tag == 9:
            for doc in scenes.find():
                if u'南投' in doc['Add']:
                    if mode == 3:
                        answer = doc_parse(doc, answer, count)
                        if count == 24:
                            return answer
                    else:
                        if count >= count2:
                            end = deal_scene(
                                count, count2, tag, doc, sender_id)
                        if end == 1:
                            break
                    count = count + 1
            if(count == 0 and mode == 1):
                bot.send_message(sender_id, "嗚嗚嗚不好意思，找不到相對應的結果")
            elif mode == 3:
                return answer
        elif tag == 10:
            for doc in scenes.find():
                if u'雲林' in doc['Add']:
                    if mode == 3:
                        answer = doc_parse(doc, answer, count)
                        if count == 24:
                            return answer
                    else:
                        if count >= count2:
                            end = deal_scene(
                                count, count2, tag, doc, sender_id)
                        if end == 1:
                            break
                    count = count + 1
            if(count == 0 and mode == 1):
                bot.send_message(sender_id, "嗚嗚嗚不好意思，找不到相對應的結果")
            elif mode == 3:
                return answer
        elif tag == 11:
            for doc in scenes.find():
                if u'嘉義' in doc['Add']:
                    if mode == 3:
                        answer = doc_parse(doc, answer, count)
                        if count == 24:
                            return answer
                    else:
                        if count >= count2:
                            end = deal_scene(
                                count, count2, tag, doc, sender_id)
                        if end == 1:
                            break
                    count = count + 1
            if(count == 0 and mode == 1):
                bot.send_message(sender_id, "嗚嗚嗚不好意思，找不到相對應的結果")
            elif mode == 3:
                return answer
        elif tag == 12:
            for doc in scenes.find():
                if u'高雄' in doc['Add']:
                    if mode == 3:
                        answer = doc_parse(doc, answer, count)
                        if count == 24:
                            return answer
                    else:
                        if count >= count2:
                            end = deal_scene(
                                count, count2, tag, doc, sender_id)
                        if end == 1:
                            break
                    count = count + 1
            if(count == 0 and mode == 1):
                bot.send_message(sender_id, "嗚嗚嗚不好意思，找不到相對應的結果")
            elif mode == 3:
                return answer
        elif tag == 13:
            for doc in scenes.find():
                if u'屏東' in doc['Add']:
                    if mode == 3:
                        answer = doc_parse(doc, answer, count)
                        if count == 24:
                            return answer
                    else:
                        if count >= count2:
                            end = deal_scene(
                                count, count2, tag, doc, sender_id)
                        if end == 1:
                            break
                    count = count + 1
            if(count == 0 and mode == 1):
                bot.send_message(sender_id, "嗚嗚嗚不好意思，找不到相對應的結果")
            elif mode == 3:
                return answer
        elif tag == 14:
            for doc in scenes.find():
                if u'宜蘭' in doc['Add']:
                    if mode == 3:
                        answer = doc_parse(doc, answer, count)
                        if count == 24:
                            return answer
                    else:
                        if count >= count2:
                            end = deal_scene(
                                count, count2, tag, doc, sender_id)
                        if end == 1:
                            break
                    count = count + 1
            if(count == 0 and mode == 1):
                bot.send_message(sender_id, "嗚嗚嗚不好意思，找不到相對應的結果")
            elif mode == 3:
                return answer
        elif tag == 15:
            for doc in scenes.find():
                if u'花蓮' in doc['Add']:
                    if mode == 3:
                        answer = doc_parse(doc, answer, count)
                        if count == 24:
                            return answer
                    else:
                        if count >= count2:
                            end = deal_scene(
                                count, count2, tag, doc, sender_id)
                        if end == 1:
                            break
                    count = count + 1
            if(count == 0 and mode == 1):
                bot.send_message(sender_id, "嗚嗚嗚不好意思，找不到相對應的結果")
            elif mode == 3:
                return answer
        elif tag == 16:
            for doc in scenes.find():
                if u'台東' in doc['Add'] or u'臺東' in doc['Add']:
                    if mode == 3:
                        answer = doc_parse(doc, answer, count)
                        if count == 24:
                            return answer
                    else:
                        if count >= count2:
                            end = deal_scene(
                                count, count2, tag, doc, sender_id)
                        if end == 1:
                            break
                    count = count + 1
            if(count == 0 and mode == 1):
                bot.send_message(sender_id, "嗚嗚嗚不好意思，找不到相對應的結果")
            elif mode == 3:
                return answer
        elif tag == 17:
            for doc in scenes.find():
                if u'澎湖' in doc['Add']:
                    if mode == 3:
                        answer = doc_parse(doc, answer, count)
                        if count == 24:
                            return answer
                    else:
                        if count >= count2:
                            end = deal_scene(
                                count, count2, tag, doc, sender_id)
                        if end == 1:
                            break
                    count = count + 1
            if(count == 0 and mode == 1):
                bot.send_message(sender_id, "嗚嗚嗚不好意思，找不到相對應的結果")
            elif mode == 3:
                return answer
        elif tag == 18:
            for doc in scenes.find():
                if u'金門' in doc['Add']:
                    if mode == 3:
                        answer = doc_parse(doc, answer, count)
                        if count == 24:
                            return answer
                    else:
                        if count >= count2:
                            end = deal_scene(
                                count, count2, tag, doc, sender_id)
                        if end == 1:
                            break
                    count = count + 1
            if(count == 0 and mode == 1):
                bot.send_message(sender_id, "嗚嗚嗚不好意思，找不到相對應的結果")
            elif mode == 3:
                return answer
        elif tag == 19:
            for doc in scenes.find():
                if u'馬祖' in doc['Add']:
                    if mode == 3:
                        answer = doc_parse(doc, answer, count)
                        if count == 24:
                            return answer
                    else:
                        if count >= count2:
                            end = deal_scene(
                                count, count2, tag, doc, sender_id)
                        if end == 1:
                            break
                    count = count + 1
            if(count == 0 and mode == 1):
                bot.send_message(sender_id, "嗚嗚嗚不好意思，找不到相對應的結果")
            elif mode == 3:
                return answer
        elif tag == 20:
            for doc in scenes.find():
                if u'連江' in doc['Add']:
                    if mode == 3:
                        answer = doc_parse(doc, answer, count)
                        if count == 24:
                            return answer
                    else:
                        if count >= count2:
                            end = deal_scene(
                                count, count2, tag, doc, sender_id)
                        if end == 1:
                            break
                    count = count + 1
            if(count == 0 and mode == 1):
                bot.send_message(sender_id, "嗚嗚嗚不好意思，找不到相對應的結果")
            elif mode == 3:
                return answer
        elif tag == 21:
            for doc in scenes.find():
                if u'琉球' in doc['Add']:
                    if mode == 3:
                        answer = doc_parse(doc, answer, count)
                        if count == 24:
                            return answer
                    else:
                        if count >= count2:
                            end = deal_scene(
                                count, count2, tag, doc, sender_id)
                        if end == 1:
                            break
                    count = count + 1
            if(count == 0 and mode == 1):
                bot.send_message(sender_id, "嗚嗚嗚不好意思，找不到相對應的結果")
            elif mode == 3:
                return answer
        elif tag == 22:
            for doc in scenes.find():
                if u'綠島' in doc['Add']:
                    if mode == 3:
                        answer = doc_parse(doc, answer, count)
                        if count == 24:
                            return answer
                    else:
                        if count >= count2:
                            end = deal_scene(
                                count, count2, tag, doc, sender_id)
                        if end == 1:
                            break
                    count = count + 1
            if(count == 0 and mode == 1):
                bot.send_message(sender_id, "嗚嗚嗚不好意思，找不到相對應的結果")
            elif mode == 3:
                return answer
        elif tag == 23:
            for doc in scenes.find():
                if u'蘭嶼' in doc['Add']:
                    if mode == 3:
                        answer = doc_parse(doc, answer, count)
                        if count == 24:
                            return answer
                    else:
                        if count >= count2:
                            end = deal_scene(
                                count, count2, tag, doc, sender_id)
                        if end == 1:
                            break
                    count = count + 1
            if(count == 0 and mode == 1):
                bot.send_message(sender_id, "嗚嗚嗚不好意思，找不到相對應的結果")
            elif mode == 3:
                return answer
        elif tag == 24:
            for doc in scenes.find():
                if u'墾丁' in doc['Add'] or u'恆春' in doc['Add'] or u'車程' in doc['Add']:
                    if mode == 3:
                        answer = doc_parse(doc, answer, count)
                        if count == 24:
                            return answer
                    else:
                        if count >= count2:
                            end = deal_scene(
                                count, count2, tag, doc, sender_id)
                        if end == 1:
                            break
                    count = count + 1
            if(count == 0 and mode == 1):
                bot.send_message(sender_id, "嗚嗚嗚不好意思，找不到相對應的結果")
            elif mode == 3:
                return answer
    return 0

# get information and send scenes in mode = 1


def deal_scene(count, count2, tag, doc, sender_id):
    print 'in deal scene'
    if(count >= count2 + 4):
        markup = types.InlineKeyboardMarkup()
        itembtn = types.InlineKeyboardButton(
            u"想看更多", callback_data="wanttowatch2 {} {}".format(count, tag))
        markup.add(itembtn)
        bot.send_message(sender_id, u"想看更多嗎?", reply_markup=markup)
        return 1
    else:
        print doc['_id']
        name = doc['Name']
        discription = doc['Toldescribe']
        lan = doc['Px']
        lat = doc['Py']
        text = "<a href=" + "\"" + \
            doc['Picture1'] + "\">" + name + "</a>"
        bot.send_message(sender_id, text=text,
                         parse_mode="HTML")
        markup = types.InlineKeyboardMarkup()
        itembtn = types.InlineKeyboardButton(
            u"導航帶我去", callback_data=str(lan) + ' ' + str(lat))
        markup.add(itembtn)
        if not discription:
            discription = "暫無簡介"
        bot.send_message(
            sender_id, text=discription, reply_markup=markup)
        return 0

# get information and merge the answer list in mode = 3


def doc_parse(doc, answer, count):
    print "in find"
    print doc['_id']
    name = doc['Name']
    longitude = doc['Px']
    latitude = doc['Py']
    thumb_url = doc['Picture1']
    Add = doc['Add']
    scene = types.InlineQueryResultVenue(id=str(count),
                                         latitude=float(latitude),
                                         longitude=float(longitude),
                                         thumb_url=thumb_url,
                                         title=name,
                                         address=Add)
    answer.append(scene)
    return answer
