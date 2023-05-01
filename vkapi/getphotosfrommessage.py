import requests


async def get_photos_info(message_id):
    bot_token = "vk1.a.enFgN44tD6SNEhBbLKVJkCB7HwXPAmGM7QEV1q4UtusQeBsqtyFk93JjoYnenjFF6FXhVxneD27aRwMF7NkrrNs9RRphE21-Umt4wWeeLwD2oXqKFLWsyTWzrcDirarl7CYd9DV8pxaMEznqvf5xjSnE9ER1fRg-leaDk2J0HNSrKAslbmF1MGrmhS6en12Yfnp1csqN0koCNtGm-82C2w"
    url = "https://api.vk.com/method/messages.getById"
    params = {
         "access_token": bot_token,
         "v": "5.131",
         "message_ids": message_id}
    response = requests.get(url, params=params)
    message = response.json()
    photos = message["response"]["items"][0]["attachments"]
    result = []
    for photo in photos:
        owner_id = photo['photo']['owner_id']
        photo_id = photo['photo']['id']
        access_key = photo['photo']['access_key']
        vk_url = f'photo{owner_id}_{photo_id}_{access_key}'
        url = photo['photo']['sizes'][-1]['url']
        result.append({'vk_url': vk_url, 'url': url})
    return result