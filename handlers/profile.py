from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler, simple_bot_handler
from FSM import fsm, Profile
from dbase import get_profile_id, clean_offerlist
from keyboards import filter_keys, prof_set_keys
from vkapi import delete_message
from random import randint
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
                   f_ch_delete,
                   f_ch_d,
                   generate_profile_forsettings,
                   f_d_height,
                   f_d_busy,
                   f_d_hobby,
                   f_d_habits,
                   f_d_children,
                   f_d_animals,
                   f_ch_km_f)

profile_router = DefaultRouter()


@simple_bot_message_handler(profile_router, filters.PayloadFilter({"command": "menu"}),
                            StateFilter(fsm=fsm, state=Profile.show, for_what=ForWhat.FOR_USER))
async def go_menu(event: SimpleBotEvent):
    pr_id = await get_profile_id(event.user_id)
    await clean_offerlist(pr_id)
    await show_menu(event)


@simple_bot_message_handler(profile_router, filters.PayloadFilter({"command": "back"}),
                            StateFilter(fsm=fsm, state=Profile.filters, for_what=ForWhat.FOR_USER))
async def go_profile(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    prof = await generate_profile_forsettings(data['pr_id'])
    await event.answer(message=prof['msg1'],
                       attachment=prof['att1'],
                       keyboard=prof_set_keys.get_keyboard())
    await event.answer(message=prof['msg2'],
                       attachment=prof['att2'])
    await fsm.set_state(state=Profile.show, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_handler(profile_router, None, filters.EventTypeFilter('message_event'),
                    filters.PayloadFilter({'command': 'profile'}),
                    StateFilter(fsm=fsm, state=Profile.desc_more, for_what=ForWhat.FOR_USER))
async def go_prof(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    await delete_message(data['del_msgs'], event.peer_id)
    prof = await generate_profile_forsettings(data['pr_id'])
    await event.api_ctx.messages.send(message=prof['msg1'],
                                      attachment=prof['att1'],
                                      keyboard=prof_set_keys.get_keyboard(),
                                      peer_id=event.peer_id,
                                      random_id=randint(2000000000, 2147483647))
    await event.api_ctx.messages.send(message=prof['msg2'],
                                      attachment=prof['att2'],
                                      peer_id=event.peer_id,
                                      random_id=randint(2000000000, 2147483647))
    await fsm.set_state(state=Profile.show, event=event, for_what=ForWhat.FOR_USER)


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


@simple_bot_message_handler(profile_router, filters.PayloadFilter({"command": "filters"}),
                            StateFilter(fsm=fsm, state=Profile.show, for_what=ForWhat.FOR_USER))
async def go_filters(event: SimpleBotEvent):
    await event.answer(message="Выбери фильтр:",
                       keyboard=filter_keys.get_keyboard())
    await fsm.set_state(state=Profile.filters, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(profile_router, filters.PayloadFilter({"command": "desc_more"}),
                            StateFilter(fsm=fsm, state=Profile.show, for_what=ForWhat.FOR_USER))
async def go_desc_more(event: SimpleBotEvent):
    await f_ch_d(event)


@simple_bot_message_handler(profile_router, filters.PayloadFilter({"command": "age_f"}),
                            StateFilter(fsm=fsm, state=Profile.filters, for_what=ForWhat.FOR_USER))
async def change_age_f(event: SimpleBotEvent):
    await f_ch_age_f(event)


@simple_bot_message_handler(profile_router, filters.PayloadFilter({"command": "sex_f"}),
                            StateFilter(fsm=fsm, state=Profile.filters, for_what=ForWhat.FOR_USER))
async def change_sex_f(event: SimpleBotEvent):
    await f_ch_sex_f(event)


@simple_bot_message_handler(profile_router, filters.PayloadFilter({"command": "km_f"}),
                            StateFilter(fsm=fsm, state=Profile.filters, for_what=ForWhat.FOR_USER))
async def change_km_f(event: SimpleBotEvent):
    await f_ch_km_f(event)


@simple_bot_handler(profile_router, None, filters.EventTypeFilter('message_event'),
                    filters.PayloadFilter({'command': 'height'}),
                    StateFilter(fsm=fsm, state=Profile.desc_more, for_what=ForWhat.FOR_USER))
async def ch_d_height(event: SimpleBotEvent):
    await f_d_height(event)


@simple_bot_handler(profile_router, None, filters.EventTypeFilter('message_event'),
                    filters.PayloadFilter({'command': 'hobby'}),
                    StateFilter(fsm=fsm, state=Profile.desc_more, for_what=ForWhat.FOR_USER))
async def ch_d_hobby(event: SimpleBotEvent):
    await f_d_hobby(event)


@simple_bot_handler(profile_router, None, filters.EventTypeFilter('message_event'),
                    filters.PayloadFilter({'command': 'habits'}),
                    StateFilter(fsm=fsm, state=Profile.desc_more, for_what=ForWhat.FOR_USER))
async def ch_d_habits(event: SimpleBotEvent):
    await f_d_habits(event)


@simple_bot_handler(profile_router, None, filters.EventTypeFilter('message_event'),
                    filters.PayloadFilter({'command': 'busy'}),
                    StateFilter(fsm=fsm, state=Profile.desc_more, for_what=ForWhat.FOR_USER))
async def ch_d_busy(event: SimpleBotEvent):
    await f_d_busy(event)


@simple_bot_handler(profile_router, None, filters.EventTypeFilter('message_event'),
                    filters.PayloadFilter({'command': 'animals'}),
                    StateFilter(fsm=fsm, state=Profile.desc_more, for_what=ForWhat.FOR_USER))
async def ch_d_animals(event: SimpleBotEvent):
    await f_d_animals(event)


@simple_bot_handler(profile_router, None, filters.EventTypeFilter('message_event'),
                    filters.PayloadFilter({'command': 'children'}),
                    StateFilter(fsm=fsm, state=Profile.desc_more, for_what=ForWhat.FOR_USER))
async def ch_d_children(event: SimpleBotEvent):
    await f_d_children(event)


@simple_bot_message_handler(profile_router, filters.PayloadFilter({"command": "delete"}),
                            StateFilter(fsm=fsm, state=Profile.show, for_what=ForWhat.FOR_USER))
async def deactivate(event: SimpleBotEvent):
    await f_ch_delete(event)


@simple_bot_message_handler(profile_router,
                            StateFilter(fsm=fsm, state=Profile.show, for_what=ForWhat.FOR_USER))
async def go_invalid(event: SimpleBotEvent):
    await event.answer(message="Я не понимаю &#128532;\n"
                               "Пожалуйста, выбери действие на клавиатуре")


@simple_bot_message_handler(profile_router,
                            StateFilter(fsm=fsm, state=Profile.filters, for_what=ForWhat.FOR_USER))
async def go_invalid_filters(event: SimpleBotEvent):
    await event.answer(message="Я не понимаю &#128532;\n"
                               "Пожалуйста, выбери действие на клавиатуре")