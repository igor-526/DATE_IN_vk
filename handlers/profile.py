from vkwave.bots.fsm import StateFilter, ForWhat, NO_STATE
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, Profile
from dbase import get_profile_id, clean_offerlist
from funcs import (show_menu,
                   f_ch_name,
                   f_ch_bdate,
                   f_ch_sex,
                   f_ch_purposes,
                   f_ch_geo,
                   f_ch_description,
                   f_ch_del_photos,
                   f_ch_add_photos,
                   f_ch_age_f,
                   f_ch_sex_f,
                   f_ch_delete)

profile_router = DefaultRouter()


@simple_bot_message_handler(profile_router, filters.PayloadFilter({"command": "menu"}),
                            StateFilter(fsm=fsm, state=Profile.show, for_what=ForWhat.FOR_USER))
async def go_menu(event: SimpleBotEvent):
    pr_id = await get_profile_id(event.user_id)
    await clean_offerlist(pr_id)
    await show_menu(event)


@simple_bot_message_handler(profile_router, filters.PayloadFilter({"command": "name"}),
                            StateFilter(fsm=fsm, state=Profile.show, for_what=ForWhat.FOR_USER))
async def change_name(event: SimpleBotEvent):
    await f_ch_name(event)


@simple_bot_message_handler(profile_router, filters.PayloadFilter({"command": "bdate"}),
                            StateFilter(fsm=fsm, state=Profile.show, for_what=ForWhat.FOR_USER))
async def change_bdate(event: SimpleBotEvent):
    await f_ch_bdate(event)


@simple_bot_message_handler(profile_router, filters.PayloadFilter({"command": "sex"}),
                            StateFilter(fsm=fsm, state=Profile.show, for_what=ForWhat.FOR_USER))
async def change_sex(event: SimpleBotEvent):
    await f_ch_sex(event)


@simple_bot_message_handler(profile_router, filters.PayloadFilter({"command": "purposes"}),
                            StateFilter(fsm=fsm, state=Profile.show, for_what=ForWhat.FOR_USER))
async def change_purposes(event: SimpleBotEvent):
    await f_ch_purposes(event)


@simple_bot_message_handler(profile_router, filters.PayloadFilter({"command": "geo"}),
                            StateFilter(fsm=fsm, state=Profile.show, for_what=ForWhat.FOR_USER))
async def change_geo(event: SimpleBotEvent):
    await f_ch_geo(event)


@simple_bot_message_handler(profile_router, filters.PayloadFilter({"command": "description"}),
                            StateFilter(fsm=fsm, state=Profile.show, for_what=ForWhat.FOR_USER))
async def change_description(event: SimpleBotEvent):
    await f_ch_description(event)


@simple_bot_message_handler(profile_router, filters.PayloadFilter({"command": "del_photos"}),
                            StateFilter(fsm=fsm, state=Profile.show, for_what=ForWhat.FOR_USER))
async def change_d_photos(event: SimpleBotEvent):
    await f_ch_del_photos(event)


@simple_bot_message_handler(profile_router, filters.PayloadFilter({"command": "add_photos"}),
                            StateFilter(fsm=fsm, state=Profile.show, for_what=ForWhat.FOR_USER))
async def change_a_photos(event: SimpleBotEvent):
    await f_ch_add_photos(event)


@simple_bot_message_handler(profile_router, filters.PayloadFilter({"command": "age_f"}),
                            StateFilter(fsm=fsm, state=Profile.show, for_what=ForWhat.FOR_USER))
async def change_age_f(event: SimpleBotEvent):
    await f_ch_age_f(event)


@simple_bot_message_handler(profile_router, filters.PayloadFilter({"command": "sex_f"}),
                            StateFilter(fsm=fsm, state=Profile.show, for_what=ForWhat.FOR_USER))
async def change_sex_f(event: SimpleBotEvent):
    await f_ch_sex_f(event)


@simple_bot_message_handler(profile_router, filters.PayloadFilter({"command": "delete"}),
                            StateFilter(fsm=fsm, state=Profile.show, for_what=ForWhat.FOR_USER))
async def deactivate(event: SimpleBotEvent):
    await f_ch_delete(event)


@simple_bot_message_handler(profile_router,
                            StateFilter(fsm=fsm, state=Profile.show, for_what=ForWhat.FOR_USER))
async def go_invalid(event: SimpleBotEvent):
    await event.answer(message="Я вас не понимаю &#128532;\n" \
                               "Пожалуйста, выберите действие на клавиатуре")
