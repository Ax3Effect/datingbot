import vkapi
import os
import vk
from mongoengine import *
from pymongo import MongoClient
from settings import *
from datetime import date
import math

connect("chat", host="mongodb://127.0.0.1")

class User(Document):
    user_id = IntField(required=True, unique=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    gender = IntField()
    stage = IntField()
    bdate = StringField()
    age = IntField()
    photo_max_orig = StringField()
    city_id = IntField()
    city_name = StringField()
    country_id = IntField()
    country_name = StringField()
    choice_gender = IntField()
    choice_age = IntField()
    photo_id = StringField()

session = vk.Session()
api = vk.API(session, v=5.63, lang="ru")
def calculate_age(day, month, year):
    today = date.today()
    return today.year - year - ((today.month, today.day) < (month, day))

group_id = main_group_id
def getMembersBulk(group_id):
    first_check = api.groups.getMembers(group_id = group_id, count=1)
    maximum = first_check["count"]
    amount = 500
    amou = math.ceil(maximum/amount)
    for c in range(0, amou):
        users = api.groups.getMembers(group_id = group_id, count=amount, offset = c*amount, 
            fields = "sex,bdate,city,country,photo_max_orig,photo_id,has_photo")
        #print(users)
        for i in users["items"]:
            if not i.get("deactivated"):
                if i.get("has_photo") == 1:
                    print(i)
                    user = User(user_id=i["id"], first_name=i["first_name"], last_name=i["last_name"],
                        gender=i.get("sex"), bdate=i.get("bdate"), photo_max_orig=i.get("photo_max_orig"), city_id=i.get("city", {}).get("id"),
                        city_name=i.get("city", {}).get("title"), country_id=i.get("country", {}).get("id"),
                        country_name=i.get("country", {}).get("title"), photo_id = i.get("photo_id"),stage=0)
                    if user["bdate"]:
                        bdate = user["bdate"]
                        bdate = bdate.split(".")
                        if len(bdate) == 3:
                            # we have age
                            day = int(bdate[0])
                            month = int(bdate[1])
                            year = int(bdate[2])
                            age = calculate_age(day, month, year)
                            
                            user.age = age
                    try:
                        user.save()
                        print("added {}".format(i["id"]))
                    except Exception:
                        pass





getMembersBulk(group_id)


#user = api.users.get(user_ids=data["user_id"], fields='sex,bdate,city,country,photo_max_orig')[0]