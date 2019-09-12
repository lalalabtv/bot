# -*- coding: utf-8 -*-
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import vk_api
import sys  
import random
from array import *
reload(sys)  
sys.setdefaultencoding('utf-8')

token = "07622f74afe7be873d144286e593fbc11feb094fc78a59d0b3d4b71ae9fe4fb27c22395afdfb5c7001e5c"
vk_session = vk_api.VkApi(token=token)

class Pyanka(object):
    def __init__(self, data, place, persons, own_number, description, link):
        self.data = data
        self.place = place
        self.persons = persons
        self.description = description
        self.link = link
        self.own_number = own_number

p0 = Pyanka('null', 'test', 'null', '0', 'null', 'null')

partys = {p0}

kolvo = 0

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
def create_keyboard(response):
    keyboard = VkKeyboard(one_time=False)
    if response == 'привет':

        keyboard.add_button('Создать пьянку', color =VkKeyboardColor.PRIMARY)
        keyboard.add_button('Найти пьянку', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Удалить пьянку', color=VkKeyboardColor.NEGATIVE)
    keyboard = keyboard.get_keyboard()
    
    return keyboard

while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print("Текст сообщения: " + str(event.text))
            print(event.user_id)
            response = event.text.lower()
            keyboard = create_keyboard(response)
            if event.from_user and response == 'привет':
                vk_session.method('messages.send', {'user_id': event.user_id,
                                                    'message': 'Привет, добро пожаловать!' + '\n' + '\n' + 'Вот список моих команд:' + '\n' + ' 👤 Создать пьянку' + '\n' + ' 👥 Найти пьянку' + '\n' + ' ❌ Удалить пьянку',
                                                    'random_id': 0,
                                                    'keyboard': keyboard})
            if event.from_user and response == 'команды':
                vk_session.method('messages.send', {'user_id': event.user_id,
                                                    'message': 'Вот список моих команд:' + '\n' + ' 👤 Создать пьянку' + '\n' + ' 👥 Найти пьянку' + '\n' + ' ❌ Удалить пьянку',
                                                    'random_id': 0})
            if event.from_user and response == 'найти пьянку':
                vk_session.method('messages.send', {'user_id': event.user_id, 'message': '🔊 Доступные пьянки: ', 'random_id': 0})
                for x in partys:
                    if x.data != 'null':
                        vk_session.method('messages.send',
                                          {'user_id': event.user_id,
                                           'message': '📆 Дата: ' + x.data + '\n' + '🏠 Место: ' + x.place + '\n' + '👥 Количество человек:' + x.persons + '\n' + '👥 Беседа:' + x.link,
                                           'random_id': 0})
            if event.from_user and response == 'удалить пьянку':
                flag = 1
                while flag == 1:
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Введите уникальный номер пьянки', 'random_id': 0})
                    for event in longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                            number = event.text
                            vk_session.method('messages.send',
                                              {'user_id': event.user_id, 'message': '🔄 Проверяем...', 'random_id': 0})
                            for x in list(partys.keys()):
                                if x.own_number == number:
                                    partys.remove(x)
                            vk_session.method('messages.send',
                                              {'user_id': event.user_id, 'message': '✅ Пьянка удалена', 'random_id': 0})
                            flag = 0
                            break
                    break

            if event.from_user and response == 'создать пьянку':
                flag = 1
                while flag == 1:
                    id = event.user_id
                    p = Pyanka('null', 'null', 'null', '0', 'null', 'null')
                    vk_session.method('messages.send',
                                      {'user_id': id, 'message': 'Введите дату', 'random_id': 0})
                    for event in longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW and not event.from_me and event.user_id == id:
                            p.data = event.text
                            vk_session.method('messages.send',
                                              {'user_id': id, 'message': 'Введите место', 'random_id': 0})
                            flag = 2
                            break
                    if flag == 2:
                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW and not event.from_me and event.user_id == id:
                                p.place = event.text
                                vk_session.method('messages.send',
                                                  {'user_id': id, 'message': 'Количество человек',
                                                   'random_id': 0})
                                flag = 3
                                break
                    if flag == 3:
                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW and not event.from_me and event.user_id == id:
                                p.persons = event.text
                                vk_session.method('messages.send',
                                                  {'user_id': id,
                                                   'message': 'Введите описание',
                                                   'random_id': 0})
                                for event in longpoll.listen():
                                    if event.type == VkEventType.MESSAGE_NEW and not event.from_me and event.user_id == id:
                                        p.description = event.text
                                        break
                                vk_session.method('messages.send',
                                                  {'user_id': id,
                                                   'message': 'Вставьте ссылку на беседу',
                                                   'random_id': 0})
                                for event in longpoll.listen():
                                    if event.type == VkEventType.MESSAGE_NEW and not event.from_me and event.user_id == id:
                                        p.link = event.text
                                        break

                                vk_session.method('messages.send',
                                                  {'user_id': id,
                                                   'message': '📆 Дата: '+ p.data +'\n' + '🏠 Место: ' + p.place + '\n' + '👥 Количество человек:' + p.persons,
                                                   'random_id': 0})
                                flag = 0
                                vk_session.method('messages.send',
                                                  {'user_id': id,
                                                   'message': 'Всё верно? (Да/Нет)',
                                                   'random_id': 0})

                                for event in longpoll.listen():
                                    if event.type == VkEventType.MESSAGE_NEW and not event.from_me and event.user_id == id:
                                        response = event.text.lower()
                                        if(response == 'да'):
                                            r = random.randrange(100000000, 999999999, 25)
                                            p.own_number = str(r)
                                            partys.add(p)
                                            vk_session.method('messages.send',
                                                              {'user_id': id,
                                                               'message': '✅ Пьянка создана!' + '\n' + '#️⃣Её уникальный номер: ' + p.own_number,
                                                               'random_id': 0})
                                            vk_session.method('messages.send',
                                                              {'user_id': id,
                                                               'message': 'Используйте его, чтобы удалить пьянку',
                                                               'random_id': 0})
                                            flag = 0
                                            kolvo = kolvo + 1
                                            break
                                        if (response == 'нет'):
                                            flag = 1
                                            break
                                break
