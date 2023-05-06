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
                      menu_router,
                      profile_router,
                      commands_router,
                      prs_name_router,
                      prs_bdate_router,
                      prs_sex_router,
                      prs_purposes_router,
                      prs_geo_router,
                      prs_description_router,
                      prs_photos_router,
                      prs_age_f_router,
                      prs_sex_f_router,
                      prs_deactivate_router,
                      reg_tg_id_router)

bot.dispatcher.add_router(menu_router)
bot.dispatcher.add_router(commands_router)
bot.dispatcher.add_router(profile_router)
bot.dispatcher.add_router(prs_name_router)
bot.dispatcher.add_router(prs_bdate_router)
bot.dispatcher.add_router(prs_sex_router)
bot.dispatcher.add_router(prs_purposes_router)
bot.dispatcher.add_router(prs_geo_router)
bot.dispatcher.add_router(prs_description_router)
bot.dispatcher.add_router(prs_photos_router)
bot.dispatcher.add_router(prs_age_f_router)
bot.dispatcher.add_router(prs_sex_f_router)
bot.dispatcher.add_router(prs_deactivate_router)
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
bot.dispatcher.add_router(reg_tg_id_router)

loop = asyncio.get_event_loop()
loop.run_until_complete(db_bind())
# loop.run_until_complete(db_reset())
print("All routers added")
bot.run_forever()
