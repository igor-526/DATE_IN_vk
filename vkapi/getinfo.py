import requests
from config import bot_token
import datetime


async def agecount(bdate):
    try:
        birthday = datetime.datetime.strptime(bdate, '%d.%m.%Y')
        today = datetime.datetime.today()
        age = today-birthday
        return age.days//365
    except:
        return None


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
    data = {'name': None, 'city_id': None, 'city_title': None, 'age': None, 'sex': None}
    data['name'] = response.get('first_name')
    data['sex'] = response.get('sex')
    if 'city' in response:
        data['city_id'] = response.get('city').get('id')
        data['city_title'] = response.get('city').get('title')
    if 'bdate' in response: data['age'] = await agecount(response.get('bdate'))
    return data