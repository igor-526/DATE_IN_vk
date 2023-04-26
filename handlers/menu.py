from vkwave.bots.fsm import StateFilter, ANY_STATE, NO_STATE, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import (SimpleBotEvent,
                         DefaultRouter,
                         simple_bot_message_handler,
                         Keyboard)
from FSM import (fsm,
                 RegistrationFSM,
                 MenuFSM,
                 ProfileFSM)
from keyboards import (reg_keys,
                       menu_keys,
                       prof_set_keys)
from funcs import gen_profile_settings
from dbase import chk_reg

menu_router = DefaultRouter()


@simple_bot_message_handler(menu_router,
                            StateFilter(fsm=fsm, state=NO_STATE, for_what=ForWhat.FOR_USER))
async def check_reg(event: SimpleBotEvent):
    status = await chk_reg(event.user_id)
    if status:
        await event.answer(message=f'Добро пожаловать, {status.name}',
                           keyboard=menu_keys.get_keyboard())
        await fsm.set_state(state=MenuFSM.menu, event=event, for_what=ForWhat.FOR_USER)
    else:
        await event.answer(message="Добро пожаловать в DATE IN!\n"
                                   "Для начала использования нужно зарегистрироваться",
                           keyboard=reg_keys.get_keyboard())
        await fsm.set_state(event=event, state=RegistrationFSM.registration, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(menu_router, filters.PayloadFilter({"command": "profile"}),
                            StateFilter(fsm=fsm, state=MenuFSM.menu, for_what=ForWhat.FOR_USER))
async def set_profile(event: SimpleBotEvent):
    await event.answer("Пару секунд..")
    message = await gen_profile_settings(event.user_id)
    await event.answer(message=message['msg1'],
                       attachment=message['att1'],
                       keyboard=prof_set_keys.get_keyboard())
    if message['msg2'] or message['att2']:
        await event.answer(message=message['msg2'],
                           attachment=message['att2'],
                           keyboard=prof_set_keys.get_keyboard())
    await fsm.set_state(state=ProfileFSM.show, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(menu_router,
                            StateFilter(fsm=fsm, state=MenuFSM.menu, for_what=ForWhat.FOR_USER))
async def menu_invalid(event: SimpleBotEvent):
    await event.answer(message="Я вас не понимаю &#128532;\n" \
                               "Пожалуйста, выберите действие на клавиатуре",
                       keyboard=menu_keys.get_keyboard())