# -*- coding: utf-8 -*-
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')

token = "07622f74afe7be873d144286e593fbc11feb094fc78a59d0b3d4b71ae9fe4fb27c22395afdfb5c7001e5c"
vk_session = vk_api.VkApi(token=token)

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
            if event.from_user and response == 'создать пьянку':
                vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'Введите дату', 'random_id': 0})
                flag = 1
                while flag == 1:
                    for event in longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                            data = event.text
                            vk_session.method('messages.send',
                                              {'user_id': event.user_id, 'message': 'Дата и время: ' + data, 'random_id': 0})
                            vk_session.method('messages.send',
                                              {'user_id': event.user_id, 'message': 'Введите место', 'random_id': 0})
                            flag = 2
                            break
                    if flag == 2:
                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                place = event.text
                                vk_session.method('messages.send',
                                                  {'user_id': event.user_id, 'message': 'Место: ' + place,
                                                   'random_id': 0})
                                flag = 0
                                break
        if event.type == VkEventType.GROUP_JOIN:
            if event.join_type == 'approved':
                vk_session.method('messages.send', {'user_id': event.user_id,
                                                    'message': 'Добро пожаловать в паблик, напиши мне *Привет*, чтобы начать работу',
                                                    'random_id': 0})
