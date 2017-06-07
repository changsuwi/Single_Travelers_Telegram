# coding=utf-8
from db import search_scene
# deal with location, every location have uniqle tag


def select_loc(message, userid, mode):
    print 'in select loc'
    if u'台南' in message:
        answer = search_scene(userid, 0, 0, 0, mode, 0)
    elif u'台北' in message:
        answer = search_scene(userid, 0, 0, 0, mode, 1)
    elif u'新北' in message:
        answer = search_scene(userid, 0, 0, 0, mode, 2)
    elif u'基隆' in message:
        answer = search_scene(userid, 0, 0, 0, mode, 3)
    elif u'桃園' in message:
        answer = search_scene(userid, 0, 0, 0, mode, 4)
    elif u'新竹' in message:
        answer = search_scene(userid, 0, 0, 0, mode, 5)
    elif u'苗栗' in message:
        answer = search_scene(userid, 0, 0, 0, mode, 6)
    elif u'台中' in message:
        answer = search_scene(userid, 0, 0, 0, mode, 7)
    elif u'彰化' in message:
        answer = search_scene(userid, 0, 0, 0, mode, 8)
    elif u'南投' in message:
        answer = search_scene(userid, 0, 0, 0, mode, 9)
    elif u'雲林' in message:
        answer = search_scene(userid, 0, 0, 0, mode, 10)
    elif u'嘉義' in message:
        answer = search_scene(userid, 0, 0, 0, mode, 11)
    elif u'高雄' in message:
        answer = search_scene(userid, 0, 0, 0, mode, 12)
    elif u'屏東' in message:
        answer = search_scene(userid, 0, 0, 0, mode, 13)
    elif u'宜蘭' in message:
        answer = search_scene(userid, 0, 0, 0, mode, 14)
    elif u'花蓮' in message:
        answer = search_scene(userid, 0, 0, 0, mode, 15)
    elif u'台東' in message or u'臺東'in message:
        answer = search_scene(userid, 0, 0, 0, mode, 16)
    elif u'澎湖' in message:
        answer = search_scene(userid, 0, 0, 0, mode, 17)
    elif u'金門' in message:
        answer = search_scene(userid, 0, 0, 0, mode, 18)
    elif u'馬祖' in message:
        answer = search_scene(userid, 0, 0, 0, mode, 19)
    elif u'連江' in message:
        answer = search_scene(userid, 0, 0, 0, mode, 20)
    elif u'琉球' in message:
        answer = search_scene(userid, 0, 0, 0, mode, 21)
    elif u'綠島' in message:
        answer = search_scene(userid, 0, 0, 0, mode, 22)
    elif u'蘭嶼' in message:
        answer = search_scene(userid, 0, 0, 0, mode, 23)
    elif u'墾丁' in message:
        answer = search_scene(userid, 0, 0, 0, mode, 24)
    else:
        answer = search_scene(userid, 0, 0, 0, mode, 30)
    return answer
