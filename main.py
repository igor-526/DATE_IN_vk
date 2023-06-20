from bot import bot
from models import db_bind
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
                      reg_tg_id_router,
                      search_engine_router,
                      match_engine_router,
                      prmd_height_router,
                      prmd_hobby_router,
                      prmd_habits_router,
                      prmd_animals_router,
                      prmd_children_router,
                      prmd_busy_router,
                      prs_km_f_router,
                      comp_cat_router,
                      comp_desc_router,
                      comp_confirm_router,
                      report_router)

bot.dispatcher.add_router(commands_router)
bot.dispatcher.add_router(menu_router)
bot.dispatcher.add_router(search_engine_router)
bot.dispatcher.add_router(match_engine_router)
bot.dispatcher.add_router(comp_cat_router)
bot.dispatcher.add_router(comp_desc_router)
bot.dispatcher.add_router(comp_confirm_router)
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
bot.dispatcher.add_router(prs_km_f_router)
bot.dispatcher.add_router(prs_deactivate_router)
bot.dispatcher.add_router(prmd_height_router)
bot.dispatcher.add_router(prmd_hobby_router)
bot.dispatcher.add_router(prmd_habits_router)
bot.dispatcher.add_router(prmd_animals_router)
bot.dispatcher.add_router(prmd_children_router)
bot.dispatcher.add_router(prmd_busy_router)
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
bot.dispatcher.add_router(report_router)

loop = asyncio.get_event_loop()
loop.run_until_complete(db_bind())
print("All routers added")
bot.run_forever()
