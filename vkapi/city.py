import requests
# from config import service_token
from pprint import pprint


async def find_city(city: str):
    bot_token = "cfd48288cfd48288cfd48288fcccc7438eccfd4cfd48288ab937f5a1ecf68a6dbf6580a"
    url = "https://api.vk.com/method/database.getCities"
    params = {"access_token": bot_token,
              "v": "5.131",
              "q": city,
              "count": "1",
              'lang': "0",
              'country_id': "643"}
    response = requests.get(url, params=params)
    response = response.json()['response']['items']
    result = {'city_title': None, 'city_id': None}
    if response != []:
        result['city_title'] = response[0]['title']
        result['city_id'] = response[0]['id']
    return result