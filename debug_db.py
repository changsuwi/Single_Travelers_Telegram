# -*- coding:utf-8 -*-
import sys
import shutil
import pymongo
import requests
import json
from imugr import upload_photo
from datetime import datetime
# Standard URI format: mongodb://[dbuser:dbpassword@]host:port/dbname
uri = 'mongodb://vic010744:vic32823@ds147711.mlab.com:47711/heroku_jvwg4955'
GOOGLE_MAP_API_KEY = 'AIzaSyBYphlCPsejaVLP29RTZTm0Wcte9ywRLdY'
client = pymongo.MongoClient(uri)


def main(argv):
    db = client.get_default_database()

    # First we'll add a few songs. Nothing is required to create the songs
    # collection; it is created automatically when we insert.
    count = 0
    scenes = db['travel']
    for doc in scenes.find():
        name = doc['Name']
        Picture1 = doc['Picture1']
        _id = doc['_id']
        px = doc['Px']
        py = doc['Py']
        query = {'_id': _id}
        add = doc['Add']
        if(not Picture1):
            print ("No.{num}   id = {_id}   no picture".format(
                num=count, _id=_id))
            scenes.update(query, {'$set': {'Picture1': "http://www.ntge.ntpc.gov.tw/images/nopic.jpg"}})


        if(type(py) == float):
            print ("No.{num}   id = {_id}  float px".format(
                num=count, _id=_id))
            scenes.update(query, {'$set': {'Px': str(px), 'Py': str(py)}})
        

        if('place_id' in doc):
            pass
        else:
            print ("No.{num}   id = {_id}   no place_id".format(
                num=count, _id=_id))
            jsondata = requests.get('https://maps.googleapis.com/maps/api/place/textsearch/json?query={search}&key={GOOGLE_MAP_API_KEY}'.format(
                search=name.encode('utf-8'), GOOGLE_MAP_API_KEY=GOOGLE_MAP_API_KEY))
            data = json.loads(jsondata.text)
            if(len(data['results']) != 0 and 'place_id' in data['results'][0]):
                place_id = data['results'][0]['place_id']
                print "place_id = " + place_id
                scenes.update(query, {'$set': {'place_id': place_id}})
                jsondata = requests.get(
                    'https://maps.googleapis.com/maps/api/place/details/json?placeid={}&key={}'.format(place_id, GOOGLE_MAP_API_KEY))
                locdata = json.loads(jsondata.text)
                locurl = locdata['result']['url']
                scenes.update(query, {'$set': {'place_url': locurl}})
            else:
                scenes.delete_many({"_id":_id})
                print ("name.{name}   id = {_id}   delete".format(
                name=name.encode('utf-8'), _id=_id))
        if(not add):
            print ("No.{num}   id = {_id}   no Add".format(
                num=count, _id=_id))
            if 'place_id' not in doc:
                scenes.delete_many({"Name":name})
                print ("name.{name}   id = {_id}   delete".format(
                name=name.encode('utf-8'), _id=_id))
            else:
                place_id = doc['place_id']
                jsondata = requests.get(
                        'https://maps.googleapis.com/maps/api/place/details/json?placeid={}&key={}'.format(place_id, GOOGLE_MAP_API_KEY))
                locdata = json.loads(jsondata.text)
                add = locdata['result']["formatted_address"]
                scenes.update(query, {'$set': {'Add': add}})


        count = count + 1
if __name__ == '__main__':
    main(sys.argv[1:])
