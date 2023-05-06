import config
from vkwave.bots import SimpleLongPollBot


bot = SimpleLongPollBot(tokens=config.bot_token, group_id=config.group_id)
