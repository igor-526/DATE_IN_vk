import requests
from config import bot_token


async def vkuser_info(user_id):
    url = "https://api.vk.com/method/users.get"
    params = {
        "access_token": bot_token,
        "user_ids": user_id,
        "fields": "city, sex, bdate",
        "name_case": "nom",
        "v": "5.131",
    }
    response = requests.get(url, params=params)
    response = response.json()['response'][0]
    data = {'name': None, 'bdate': None, 'sex': None}
    data['name'] = response.get('first_name')
    if 'sex' in response:
        data['sex'] = response.get('sex')
    if 'bdate' in response: data['bdate'] = response.get('bdate')
    return data