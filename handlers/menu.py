from vkwave.bots.fsm import StateFilter, ForWhat, NO_STATE
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, Menu, Profile
from keyboards import yesnoback_keys, back_keys, reg_keys, prof_set_keys
from validators import valid_bdate, valid_year
from dbase import chk_reg
from funcs import start_registration, show_menu, generate_profile_forsettings

menu_router = DefaultRouter()


@simple_bot_message_handler(menu_router, filters.PayloadFilter({"command": "registration"}),
                            StateFilter(fsm=fsm, state=NO_STATE, for_what=ForWhat.FOR_USER))
async def reg(event: SimpleBotEvent):
    await start_registration(event)


@simple_bot_message_handler(menu_router,
                            StateFilter(fsm=fsm, state=NO_STATE, for_what=ForWhat.FOR_USER))
async def start(event: SimpleBotEvent):
    check = await chk_reg(event.user_id)
    if check:
        await event.answer(message=f"Добро пожаловать, {check.name}")
        await show_menu(event)
    else:
        await event.answer(message="Добро пожаловать в DATE IN!\n"
                                   "Для начала использования необходимо зарегистрироваться",
                           keyboard=reg_keys.get_keyboard())


@simple_bot_message_handler(menu_router, filters.PayloadFilter({"command": "profile"}),
                            StateFilter(fsm=fsm, state=Menu.menu, for_what=ForWhat.FOR_USER))
async def profile(event: SimpleBotEvent):
    prof = await generate_profile_forsettings(event.user_id)
    await event.answer(message=prof['msg1'],
                       attachment=prof['att1'],
                       keyboard=prof_set_keys.get_keyboard())
    await event.answer(message=prof['msg2'],
                       attachment=prof['att2'])
    await fsm.set_state(state=Profile.show, event=event, for_what=ForWhat.FOR_USER)
