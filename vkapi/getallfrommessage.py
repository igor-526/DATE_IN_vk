import requests
from config import bot_token


async def get_message(message_id):
    url = "https://api.vk.com/method/messages.getById"
    params = {
         "access_token": bot_token,
         "v": "5.131",
         "message_ids": message_id}
    response = requests.get(url, params=params)
    message = response.json()
    text = message['response']['items'][0]['text']
    photos = message["response"]["items"][0]["attachments"]
    result = {'text': text, 'photos': []}
    for photo in photos:
        owner_id = photo['photo']['owner_id']
        photo_id = photo['photo']['id']
        access_key = photo['photo'].get('access_key')
        vk_url = f'photo{owner_id}_{photo_id}_{access_key}' if access_key else f'photo{owner_id}_{photo_id}'
        url = photo['photo']['sizes'][-1]['url']
        result['photos'].append({'vk_url': vk_url, 'url': url})
    return result
