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
            if event.from_user:
                if response == 'привет':
                    vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'Привет, добро пожаловать!', 'random_id': 0})
