import requests
import time
from pprint import pprint

with open('token.txt') as f:
    access_token = f.read()
first_user_id = 72625041
second_user_id = 145594749
frlist =list()

class User:

    def __init__(self, id):
        self.token = access_token
        self.id = id
        self.link = 'https://vk.com/id' + str(self.id)
    def __str__(self):
        return self.link

    def get_mutual_friends(self, user_id, target_id):
        self.user_id = user_id
        self.target_id = target_id
        mutual_friends = list()
        first_user = requests.get('https://api.vk.com/method/users.get',
                                  params={'access_token': access_token, 'user_id': user_id, 'v': '5.52',
                                          'fields': ['first_name', 'last_name']}).json()['response']
        name_surname_1 = first_user[0]['first_name'] + ' ' + first_user[0]['last_name']

        second_user = requests.get('https://api.vk.com/method/users.get',
                                   params={'access_token': access_token, 'user_id': target_id, 'v': '5.52',
                                           'fields': ['first_name', 'last_name']}).json()['response']
        name_surname_2 = second_user[0]['first_name'] + ' ' + second_user[0]['last_name']

        params = {'access_token': access_token,
                  'source_uid': user_id,
                  'target_uid': target_id,
                  'v': '5.52'}
        response = requests.get('https://api.vk.com/method/friends.getMutual', params=params)
        for ID in response.json()['response']:
            response_params = {'access_token': access_token,
                               'user_id': ID,
                               'v': '5.52',
                               'fields': ['first_name', 'last_name']}
            friend = requests.get('https://api.vk.com/method/users.get', params=response_params)
            mutual_friends.append(friend.json())
            time.sleep(0.3)
            print('running...')
        print(f'Общие друзья: у {name_surname_1} и {name_surname_2}:')
        for data in mutual_friends:
            resp = data['response'][0]
            first_name = resp['first_name']
            last_name = resp['last_name']
            ID = str(resp['id'])
            link = 'https://vk.com/id' + ID
            frlist.append(f'{first_name} {last_name}: {link}')
        return frlist
    def __and__(self, other):
        return self.get_mutual_friends(user_id=self.id, target_id=other.id)


user = User(72625041)
print(user)

user2 = User(145594749)
pprint(user & user2)