# -*- coding: utf-8 -*-
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
import sys  
from array import *
reload(sys)  
sys.setdefaultencoding('utf-8')

token = "07622f74afe7be873d144286e593fbc11feb094fc78a59d0b3d4b71ae9fe4fb27c22395afdfb5c7001e5c"
vk_session = vk_api.VkApi(token=token)

class Pyanka(object):
    def __init__(self, data, place, persons):
        self.data = data
        self.place = place
        self.persons = persons

p0 = Pyanka('null', 'test', 'null')

partys = {p0}

kolvo = 0

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print("Текст сообщения: " + str(event.text))
            print(event.user_id)
            response = event.text.lower()
            if event.from_user and response == 'привет':
                vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'Привет, добро пожаловать!', 'random_id': 0})
            if event.from_user and response == 'показать пьянки':
                vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'Доступные пьянки: ', 'random_id': 0})
                for x in partys:
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id,
                                       'message': 'Дата: '+ x.data +'\n' + 'Место: ' + x.place + '\n' + 'Количество человек:' + x.persons,
                                       'random_id': 0})

            if event.from_user and response == 'создать пьянку':
                p = Pyanka('null','null','null')
                vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'Введите дату', 'random_id': 0})
                flag = 1
                while flag == 1:
                    for event in longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                            p.data = event.text
                            vk_session.method('messages.send',
                                              {'user_id': event.user_id, 'message': 'Дата и время: ' + p.data, 'random_id': 0})
                            vk_session.method('messages.send',
                                              {'user_id': event.user_id, 'message': 'Введите место', 'random_id': 0})
                            flag = 2
                            break
                    if flag == 2:
                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                p.place = event.text
                                vk_session.method('messages.send',
                                                  {'user_id': event.user_id, 'message': 'Место: ' + p.place,
                                                   'random_id': 0})
                                vk_session.method('messages.send',
                                                  {'user_id': event.user_id, 'message': 'Количество человек',
                                                   'random_id': 0})
                                flag = 3
                                break
                    if flag == 3:
                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                p.persons = event.text
                                vk_session.method('messages.send',
                                                  {'user_id': event.user_id, 'message': 'Количество человек: ' + p.persons,
                                                   'random_id': 0})
                                vk_session.method('messages.send',
                                                  {'user_id': event.user_id,
                                                   'message': 'Пьянка создана!',
                                                   'random_id': 0})
                                flag = 0
                                partys.add(p)
                                kolvo = kolvo+1
                                break
