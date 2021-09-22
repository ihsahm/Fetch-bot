import datetime
import re
from firebase_admin import firestore
from firebase_admin import credentials
import firebase_admin
import pyrebase
from telethon import TelegramClient, events
import logging

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)

api_id = "785998"
api_hash = "cec86f97760ef536378a9accebf941f2"
client = TelegramClient("anon", api_id, api_hash)
config = {
    "apiKey": "AIzaSyBhkHRBylcisBl2avB_kypbUZ85dAOOmAA",
    "authDomain": "tikvah-news.firebaseapp.com",
    "databaseURL": "https://tikvah-news.firebaseio.com",
    "projectId": "tikvah-news",
    "storageBucket": "tikvah-news.appspot.com",
    "messagingSenderId": "54814125934",
    "appId": "1:54814125934:web:ab26afcdf405e87ee01b7f",
    "measurementId": "G-D8EF4SD1PY",
}
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
cred = credentials.Certificate("tikvah-news-firebase-adminsdk-x5hzx-73b3bf37b1.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
doc_ref = db.collection("sportlist")


async def main():

    # car_names = list(dict.fromkeys(car_names))
    i = 0
    # k = 0
    # nap = 0
    imgarr = []
    # car_detail = {
    #     "image": [],
    #     "whole": "",
    # }

    async for message in client.iter_messages("@tikvahethsport"):
        if message.text:
            if imgarr != []:
                print("uploaded")
                imgarr = list(dict.fromkeys(imgarr))
                doc_ref.document("fcm" + str(i)).set(
                    {
                        "image": imgarr,
                        "whole-text": message.text,
                        "time": datetime.datetime.now(),
                    }
                )
            imgarr = []

        if message.photo:
            path = await message.download_media("/home/ihs/Desktop/Images")
            path_on_cloud = "sportimage/" + str(i) + ".jpg"
            storage.child(path_on_cloud).put(path)
            i += 1
            ur = storage.child(path_on_cloud).get_url(str(i) + ".jpg")
            imgarr.append(ur)


with client:
    client.loop.run_until_complete(main())
