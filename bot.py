import config
from vkwave.bots import SimpleLongPollBot, SimpleCallbackBot


bot = SimpleLongPollBot(tokens=config.bot_token, group_id=config.group_id)

# bot = SimpleCallbackBot(
#     group_id=config.group_id,
#     host="127.0.0.1",
#     path="",
#     port=3001,
#     tokens=config.bot_token,
#     confirmation_key="f05fe273",
#     secret="zhrVWfxtL1jBCR2qUezC",
# )
