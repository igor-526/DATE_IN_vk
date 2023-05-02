from bot import bot
from models import db_bind, db_reset
import asyncio
from handlers import (reg_profile_router,
                      reg_name_router,
                      reg_bdate_router,
                      reg_geo_router,
                      reg_photo_router,
                      reg_description_router,
                      reg_purposes_router,
                      reg_sexf_router,
                      reg_age_min_router,
                      reg_age_max_router,
                      reg_sex_router,
                      menu_router)

bot.dispatcher.add_router(reg_profile_router)
bot.dispatcher.add_router(reg_name_router)
bot.dispatcher.add_router(reg_bdate_router)
bot.dispatcher.add_router(reg_sex_router)
bot.dispatcher.add_router(reg_geo_router)
bot.dispatcher.add_router(reg_photo_router)
bot.dispatcher.add_router(reg_description_router)
bot.dispatcher.add_router(reg_purposes_router)
bot.dispatcher.add_router(reg_sexf_router)
bot.dispatcher.add_router(reg_age_min_router)
bot.dispatcher.add_router(reg_age_max_router)
bot.dispatcher.add_router(menu_router)

loop = asyncio.get_event_loop()
loop.run_until_complete(db_bind())
# loop.run_until_complete(db_reset())
print("All routers added")
bot.run_forever()