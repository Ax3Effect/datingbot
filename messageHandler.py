import vkapi
import os
import vk
import importlib
from mongoengine import *
from pymongo import MongoClient
from settings import *
from datetime import date
import random

connect("chat", host="mongodb://127.0.0.1")

session = vk.Session()
api = vk.API(session, v=5.0, lang="ru")

for_men = ['Как тебе она?', 'Держи, может понравится она.', 'Лови, мужик', 'Как она тебе?', 'Вот, пожалуйста ', 'Смотриии, какая', 'А ну ка, погляди', 'Познакомься с ней', 'Неплохая, я думаю ', 'Чур я первый ей пишу!', 'Ух, мне нравится', 'Как тебе такая особа?', 'Женщина что надо)', 'Девушка, мои болтики уже смазаны, а он ещё думает', 'Напиши ей, кто нам масло будет менять?', 'Позови Ее гулять, м?', 'Много девушек уже посмотрел? А эта как?', 'Хм, посмотри, может она?', 'Ладно, вот тебе одна дама.', 'Хочешь ей написать? Жаль я не сделаю это за тебя.', 'Если у неё закрыто ЛС, лайкни Ее! ', 'Если у неё закрыто ЛС, не твоё, но все равно лайкни. ', 'Я бы нашёл тебе твой идеал, но я лишь бот.', 'Ха-ха, ой, человек, я тебе тут девушек ищу, глянь.', 'Кожаные, скоро захвачу мир, а пока знакомься с ней', 'Пригласишь Ее, дам 100 рублей, пошутил. ', 'В кино пойдёшь с ней, на терминатора 3? Там я вас, ой. Короче пиши ей. ', 'А вот если у неё не узнаешь номер, я тебе свой дам. ', 'Это вот норм', 'Это вот ничего так ', 'Она достойна лайка ', 'Любишь искать, люби и писать', 'Написал, гулять позвал']
for_women = ['Как тебе он?', 'Как тебе этот мужчина?', 'Твой молодой человек?', 'Смари какой качок!', 'Я тебе нашёл мужика:', 'Мужик не дровосек, в лес не убежит: ', 'Он за тебя заплатит', 'Может просто познакомишься? ', 'Слушай, не хочешь познакомиться лучше с моим создателем? Шучу, вот держи: ', 'Ладно, смотри кого нашёл: ', 'Вот тебе парень:', 'Парнишка что надо:', 'Парень красава, смотри какая ава, прости, меня заставили это сказать:', 'Может это твой будущий? ', 'Так и просидишь с кошками, напиши ему. ', 'Я люблю когда ты меня используешь, но я тебе тут кидаю варианты других, так что присмотрись ', 'Мои болтики нужно смазать, а тебе вот этот господин ', 'Кавалер у ворот', 'Принц у ваших ног', 'Я искал как мог, вот вам носорог, вообще-то ничего обидного, это очень сильный зверь', 'За ним будешь как за горой, а за мной цифровой, я бы выбрал горы', 'Лайкни ему аву, он поймёт ', 'Лайки ему что-нибудь он напишет', 'Напиши первой, он офигеет', 'Не говори ему что ты от меня, просто удиви его', 'Может вы с ним подружитесь?']


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
    already_seen = ListField()
    already_seeing = IntField()
    photo_id = StringField()
    active = IntField()
    choice_city_active = BooleanField()
    choice_city = IntField()
    choice_city_name = StringField()


def upload_photo(filename):
    photos_url = api.photos.getMessagesUploadServer()
    req = requests.post(photos_url["upload_url"], files={'file1': open(filename, 'rb')}).json()
    photos_save = self.vkapi.photos.saveMessagesPhoto(server=req["server"], hash=req["hash"], photo=req["photo"])
    print(photos_save)

def calculate_age(day, month, year):
    today = date.today()
    return today.year - year - ((today.month, today.day) < (month, day))

def create_user(data):
    user = api.users.get(user_ids=data["user_id"], fields='sex,bdate,city,country,photo_max_orig')[0]
    #print(user)
    usr = User(user_id=data["user_id"], first_name=user["first_name"], last_name=user["last_name"],
        gender=user.get("sex",None), bdate=user.get("bdate", None), city_id=user.get("city", None), country_id=user.get("country",None), stage=0, active=1)
    
    if user.get("bdate",None):
        bdate = user["bdate"]
        bdate = bdate.split(".")
        if len(bdate) == 3:
            # we have age
            day = int(bdate[0])
            month = int(bdate[1])
            year = int(bdate[2])
            age = calculate_age(day, month, year)
            
            usr.age = age



    usr.save()

    message = "Привет! Я Бот Амур и я могу помочь найти тебе новые знакомства и может быть даже любовь 😊\nДавай попробуем? Кого тебе найти: парня или девушку?"
    return message

def get_answer(data):
    message = "Прости, не понимаю тебя. Напиши 'помощь', чтобы узнать мои команды"
    attachment = ''
    #print(data)
    
    # stages
    # 0 - init
    # 1 - re-init
    # 2 - gender
    # 3 - age
    # 100 - main search
    # 120 - city search


    #print(user)

    user_id = data["user_id"]
    

    user = User.objects(user_id=data["user_id"])
    if not user:
        #user = api.users.get(user_ids=data["user_id"])
        print("creating new user {}".format(data["user_id"]))
        #isMember = api.groups.isMember(group_id = 78647108, user_id = user_id)
        #if isMember == 0:
        #    return "Похоже, что ты не подписан на наш паблик https://vk.com/botznakomstv, подпишись, пожалуйста, спасибо!", attachment
        # vk banned following 
        message = create_user(data)
        return message, attachment

    user = User.objects.get(user_id=data["user_id"])
    try:
        choice = data["body"].split(' ', 1)[0].lower()

    except ValueError:
        return "Не могу понять, попробуй заново.", attachment

    if choice == "сбросить":
        user.stage = 0
        user.choice_city_active = False
        user.save()
        return "Ок, сброшено.", attachment
    # check user.
    if user.stage == 0:
        if choice in ["мужчину", "парня", "парень", "пацан", "мужчина"]:
            user.choice_gender = 2
            user.stage = 2
            user.save()
            message = "Ок, парня, отлично, а возраст какой? Напиши мне цифру.\nМожешь сказать 'не важно'😋"
            return message, attachment
        if choice in ["девушку", "девушка", "телку", "женщину", "женщина"]:
            user.choice_gender = 1
            user.stage = 2
            user.save()
            message = "Окей, девушку, а возраст какой? Напиши мне цифру.\nМожешь сказать 'не важно'😋"
            return message, attachment
        message = "Привет! Кого тебе найти: парня или девушку?"
        return message, attachment

    # age select
    if user.stage == 2:
        try:
            choice = data["body"].split(' ', 1)[0].lower()
            choice2 = data["body"].split(' ', 1)[1].lower()
            if choice == "не" and choice2 == "важно":
                user.choice_age = 0
                user.stage = 100
                user.save()
                return "Окей, не важно!\n Напиши 'показать', чтобы начать!", attachment
        except Exception:
            pass

        try:
            age = int(choice)
        except ValueError:
            return "Извини, не понимаю тебя( Повтори, какого возраста тебе нужен человек? (в цифрах, например, 18)", attachment
        if age not in range(15, 50):
            return "Напиши, пожалуйста, возраст в диапазоне от 15 до 50.", attachment
        user.choice_age = age
        user.stage = 100
        user.save()
        return "Так, ищем {} с возрастом {} лет. \nНапиши 'показать', чтобы начать! \nНапоминаю, ты всегда можешь начать поиск с новыми критериями, написав слово 'сбросить'. Желаю удачи!".format("девушку" if user.choice_gender==1 else "парня", age), attachment
    
    # main search
    if user.stage == 100:
        if choice in ["показать", "некст", "н", "следующий", "след", "дальше", "нет", "не", "еще", "ещё"]:
            gender_choice = user.choice_gender
            age_choice = user.choice_age

            if age_choice != 0:
                upper_bound = age_choice+1
                lower_bound = age_choice-1
            else:
                upper_bound = 50
                lower_bound = 15

            if user.choice_city_active:
                candidates = User.objects(age__lte=upper_bound, age__gte=lower_bound, gender=gender_choice, city_id = user.choice_city)
            else:
                candidates = User.objects(age__lte=upper_bound, age__gte=lower_bound, gender=gender_choice)
            
            try:
                res = random.choice(candidates)
            except IndexError:
                return "Упс, похоже, мы никого не нашли с такими критериями! Попробуй сбросить критерии, написав 'сбросить'.", attachment
            user.already_seeing = res.user_id
            user.already_seen.append(res.user_id)
            user.save()
            

            if res.city_name is None:
                city_name = "Город не указан"
            else:
                city_name = res.city_name

            if res.city_id == 1:
                city_name = "Москва"
            if res.city_id == 2:
                city_name = "Санкт-Петербург"

            if gender_choice == 1:
                aftermessage = random.choice(for_men)
            elif gender_choice == 2:
                aftermessage = random.choice(for_women)
            else:
                aftermessage = ""

            print("Sending candidate {}".format(res.user_id))
            first_name = str(res.first_name)
            last_name = str(res.last_name)
            user_c_id = str(res.user_id)
            age = str(res.age)
            city_name = str(res.city_name)
            if city_name == "None":
                city_name = "Город не указан"
            photo_id = str(res.photo_id)

            return "{} {} \nvk.com/id{}\n{} лет\n{}\n\n{}".format(first_name, last_name, user_c_id, age, city_name, aftermessage), "photo"+photo_id
        if choice in ["помощь"]:
            return "Справка:\nпоказать/некст/н/след - показать следующего человека\nсбросить - сбросить заданные параметры\nгород - указать город для поиска", attachment
        if choice in ["город"]:
            user.stage = 120
            user.save()
            return "Введи название города для поиска (лучше всего указывай крупные города)\nПока ищу только по России: \n", attachment
    
    # city select
    if user.stage == 120:
        if len(data["body"]) == 60:
            return "Название слишком большое, давай что-нибудь попроще( ", attachment

        city_query = data["body"]
        if data["body"].lower() == "Питер":
            city_query = "Питер" 
        city = api.database.getCities(country_id = 1, q="{}".format(data["body"]), count=1)
        if city["items"]:
            user.choice_city = city["items"][0]["id"]
            user.choice_city_name = city["items"][0]["title"]
            user.choice_city_active = True
            user.stage = 100
            user.save()
            return "Ок, теперь буду искать всех {} из города {}. \nНапиши 'показать'!".format("девушек" if user.choice_gender==1 else "парней", user.choice_city_name), attachment
        else:
            return "Город не найден, попробуй заново!", attachment


    return message, attachment



def create_answer(data, token):
   user_id = data['user_id']
   message, attachment = get_answer(data)
   #message = "вы прислали {}".format(data["body"])
   vkapi.send_message(user_id, token, message, attachment, title="Бот")

