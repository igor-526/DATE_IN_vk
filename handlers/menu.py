from vkwave.bots.fsm import StateFilter, ForWhat, NO_STATE
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, MenuFSM
from keyboards import yesnoback_keys, back_keys, reg_keys
from validators import valid_bdate, valid_year
from dbase import chk_reg
from funcs import start_registration

menu_router = DefaultRouter()


@simple_bot_message_handler(menu_router, filters.PayloadFilter({"command": "registration"}),
                            StateFilter(fsm=fsm, state=NO_STATE, for_what=ForWhat.FOR_USER))
async def reg(event: SimpleBotEvent):
    await start_registration(event)


@simple_bot_message_handler(menu_router,
                            StateFilter(fsm=fsm, state=NO_STATE, for_what=ForWhat.FOR_USER))
async def start(event: SimpleBotEvent):
    await event.answer(message="Добро пожаловать в DATE IN!\n"
                               "Для начала использования необходимо зарегистрироваться",
                       keyboard=reg_keys.get_keyboard())