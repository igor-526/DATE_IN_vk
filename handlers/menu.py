from vkwave.bots.fsm import StateFilter, ForWhat, NO_STATE
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, Menu, Profile, Search
from keyboards import reg_keys, prof_set_keys, return_keys, search_keys, newmatch_keys
from dbase import chk_reg, dates_info, upd_activate_profile, upd_delete_profile, get_profile_id
from funcs import (start_registration,
                   show_menu,
                   generate_profile_forsettings,
                   f_ch_geo,
                   search,
                   show_new_match,
                   menu_invalid)
import datetime
import pytz

menu_router = DefaultRouter()


@simple_bot_message_handler(menu_router, filters.PayloadFilter({"command": "registration"}),
                            StateFilter(fsm=fsm, state=NO_STATE, for_what=ForWhat.FOR_USER))
async def reg(event: SimpleBotEvent):
    await start_registration(event)


@simple_bot_message_handler(menu_router, filters.PayloadFilter({"command": "return"}),
                            StateFilter(fsm=fsm, state=NO_STATE, for_what=ForWhat.FOR_USER))
async def ret_profile(event: SimpleBotEvent):
    await upd_activate_profile(event.user_id)
    await event.answer(message='Профиль успешно восстановлен!')
    await show_menu(event)


@simple_bot_message_handler(menu_router,
                            StateFilter(fsm=fsm, state=NO_STATE, for_what=ForWhat.FOR_USER))
async def start(event: SimpleBotEvent):
    check = await chk_reg(event.user_id)
    if check:
        if check.status == 'active':
            await event.answer(message=f"Добро пожаловать, {check.name}")
            await show_menu(event)
        elif check.status == 'deactivated':
            datesinfo = await dates_info(event.user_id)
            if datesinfo['deactivated'] > datetime.datetime.now().replace(tzinfo=pytz.utc)-datetime.timedelta(days=7):
                await event.answer(message=f'Добро пожаловать, {check.name}\n'
                                           f'Твой профиль будет удалён '
                                           f'{datesinfo["deactivated"]+datetime.timedelta(days=7)}\n'
                                           f'Хочешь восстановить профиль сейчас?',
                                   keyboard=return_keys.get_keyboard())
            else:
                await upd_delete_profile(event.user_id)
                await event.answer(message="Добро пожаловать в DATE IN!\n"
                                           "Для начала использования необходимо зарегистрироваться",
                                   keyboard=reg_keys.get_keyboard())
    else:
        await event.answer(message="Добро пожаловать в DATE IN!\n"
                                   "Для начала использования необходимо зарегистрироваться",
                           keyboard=reg_keys.get_keyboard())


@simple_bot_message_handler(menu_router, filters.PayloadFilter({"command": "start"}),
                            StateFilter(fsm=fsm, state=Menu.menu, for_what=ForWhat.FOR_USER))
async def start_search(event: SimpleBotEvent):
    await fsm.set_state(state=Search.searching, for_what=ForWhat.FOR_USER, event=event)
    await event.answer(message="Уже ищу..",
                       keyboard=search_keys.get_keyboard())
    pr_id = await get_profile_id(event.user_id)
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'pr_id': pr_id})
    await search(event)


@simple_bot_message_handler(menu_router, filters.PayloadFilter({"command": "upd_geo"}),
                            StateFilter(fsm=fsm, state=Menu.menu, for_what=ForWhat.FOR_USER))
async def upd_geo(event: SimpleBotEvent):
    pr_id = await get_profile_id(event.user_id)
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'pr_id': pr_id})
    await f_ch_geo(event)
    await fsm.set_state(state=Menu.geo, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(menu_router, filters.PayloadFilter({"command": "profile"}),
                            StateFilter(fsm=fsm, state=Menu.menu, for_what=ForWhat.FOR_USER))
async def profile(event: SimpleBotEvent):
    pr_id = await get_profile_id(event.user_id)
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'pr_id': pr_id})
    prof = await generate_profile_forsettings(pr_id)
    await event.answer(message=prof['msg1'],
                       attachment=prof['att1'],
                       keyboard=prof_set_keys.get_keyboard())
    await event.answer(message=prof['msg2'],
                       attachment=prof['att2'])
    await fsm.set_state(state=Profile.show, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(menu_router, filters.PayloadFilter({"command": "matches"}),
                            StateFilter(fsm=fsm, state=Menu.menu, for_what=ForWhat.FOR_USER))
async def matches(event: SimpleBotEvent):
    pr_id = await get_profile_id(event.user_id)
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'pr_id': pr_id})
    await event.answer(message="Секунду..",
                       keyboard=newmatch_keys.get_keyboard())
    await show_new_match(event)


@simple_bot_message_handler(menu_router,
                            StateFilter(fsm=fsm, state=Menu.menu, for_what=ForWhat.FOR_USER))
async def invalid(event: SimpleBotEvent):
    await menu_invalid(event)
