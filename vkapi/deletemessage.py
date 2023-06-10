import requests
from config import bot_token


async def delete_message(messages, peer_id):
    url = "https://api.vk.com/method/messages.delete"
    for msg in messages:
        params = {
             "access_token": bot_token,
             "v": "5.131",
             "message_ids": msg,
             "peer_id": peer_id,
             "delete_for_all": 1}
        requests.get(url, params=params)
