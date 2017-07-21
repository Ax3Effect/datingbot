import vkapi
import os
import vk
import importlib
from command_system import command_list
from mongoengine import *
from pymongo import MongoClient
from settings import *
from datetime import date
import random
import time

session = vk.Session(access_token=token)
api = vk.API(session, v=5.0, lang="ru")
client = MongoClient('localhost', 27017)
def gather_users():
    db = client.chat
    collection = db.user
    all_users = []

    for user in collection.find({'already_seen':{"$exists":True}, "$where":'this.already_seen.length>10'}):
        all_users.append(user["user_id"])

    return all_users

users = gather_users()
print("Sending mass message to {} users".format(len(users)))

mass_message = '''
Привет, тебя беспокоит администрация паблика *botznakomstv ( Обычные знакомства ). 😊 

Появились новые фишки бота, а именно: 

1. Выбор города 
2. Выбор возраста ( upgrade ) 
3. Каждую неделю бот будет самостоятельно поощрять активных пользователей - дарить стикеры.

Также, мы подключили к сообществу функцию анализа и каждый лайк/комментарий прибавляет к вашему ID-страницы баллы. Количество баллов можно будет узнать 1 июня. Кто попадет в 50 активных пользователей, получит главные призы.

Пригласив в группу друзей в паблик можно получить максимальное количество баллов, удачи! 
Мы вас любим ❤





'''

count = 1
for i in users:
    isallowed = api.messages.isMessagesFromGroupAllowed(group_id=main_group_id, user_id=i)

    #print(isallowed)
    time.sleep(0.5)
    if isallowed["is_allowed"] == 1:
        print("Sending msg to {} ({}/{})".format(i, count, len(users)))
        api.messages.send(user_id=i, message=mass_message)
        time.sleep(0.5)

    count += 1
    
