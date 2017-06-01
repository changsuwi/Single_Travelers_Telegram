# -*- coding: utf-8 -*-
"""
Created on Sat May 06 19:29:08 2017
運用google api抓圖，並將圖片抓至imgur，再將回傳的url存至DB
@author: vicharm
"""

# -*- coding:utf-8 -*-
import sys
import shutil
import pymongo
import requests
import json
from imugr import upload_photo
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
# Standard URI format: mongodb://[dbuser:dbpassword@]host:port/dbname
uri = 'mongodb://vic010744:vic32823@ds147711.mlab.com:47711/heroku_jvwg4955'
GOOGLE_MAP_API_KEY = 'AIzaSyBYphlCPsejaVLP29RTZTm0Wcte9ywRLdY'


def job_function():

    client = pymongo.MongoClient(uri)

    db = client.get_default_database()

    count = 0
    scenes = db['travel']
    for doc in scenes.find():
        name = doc['Name']
        Picture1 = doc['Picture1']
        _id = doc['_id']
        if(not Picture1):
            print ("No.{num}   id = {_id}".format(num=count, _id=_id))
            jsondata = requests.get('https://maps.googleapis.com/maps/api/place/textsearch/json?query={search}&key={GOOGLE_MAP_API_KEY}'.format(
                search=name.encode('utf-8'), GOOGLE_MAP_API_KEY=GOOGLE_MAP_API_KEY))
            data = json.loads(jsondata.text)
            if(len(data['results']) != 0 and 'photos' in data['results'][0]):

                photo_reference = data['results'][0][
                    'photos'][0]['photo_reference']
                photo_url = requests.get('https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={GOOGLE_MAP_API_KEY}'.format(
                    photo_reference=photo_reference, GOOGLE_MAP_API_KEY=GOOGLE_MAP_API_KEY), stream=True)
                image_path = name + '.png'
                with open(image_path, 'wb') as out_file:
                    shutil.copyfileobj(photo_url.raw, out_file)
                del photo_url

                link = upload_photo(image_path)
                count = count + 1

                query = {'Name': name}
                scenes.update(query, {'$set': {'Picture1': link}})
                client.close()
                if(count == 40):
                    break
            else:
                print "pass"


def main(argv):
    sched = BlockingScheduler()
    sched.add_job(job_function, 'interval', hours=1)

    sched.start()

if __name__ == '__main__':
    main(sys.argv[1:])
