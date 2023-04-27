from bot import bot
from handlers import (reg_profile_router,
                      reg_name_router,
                      profile_sets_router,
                      menu_router)
from models import db_bind, db_reset
import asyncio

bot.dispatcher.add_router(reg_profile_router)
bot.dispatcher.add_router(reg_name_router)
bot.dispatcher.add_router(profile_sets_router)
bot.dispatcher.add_router(menu_router)
loop = asyncio.get_event_loop()
loop.run_until_complete(db_bind())
loop.run_until_complete(db_reset())
print("All routers added")
bot.run_forever()