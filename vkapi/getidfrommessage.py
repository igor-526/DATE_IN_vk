import requests
from config import bot_token


async def get_id_from_message(message_id, peer_id):
    url = "https://api.vk.com/method/messages.getByConversationMessageId"
    params = {
         "access_token": bot_token,
         "v": "5.131",
         "conversation_message_ids": message_id,
         "peer_id": peer_id}
    response = requests.get(url, params=params)
    message = response.json()['response']['items'][0]['text']
    message = message.split('(')[1]
    message = message.split(')')[0]
    pr_id = message[1:]
    return int(pr_id)
