from vkwave.bots.fsm import StateFilter, ForWhat, NO_STATE
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, Menu, Profile
from keyboards import yesnoback_keys, back_keys, reg_keys, prof_set_keys
from validators import valid_bdate, valid_year
from dbase import chk_reg
from funcs import start_registration, show_menu, generate_profile_forsettings

profile_router = DefaultRouter()


@simple_bot_message_handler(profile_router, filters.PayloadFilter({"command": "menu"}),
                            StateFilter(fsm=fsm, state=Profile.show, for_what=ForWhat.FOR_USER))
async def go_menu(event: SimpleBotEvent):
    await show_menu(event)


@simple_bot_message_handler(profile_router,
                            StateFilter(fsm=fsm, state=Profile.show, for_what=ForWhat.FOR_USER))
async def go_invalid(event: SimpleBotEvent):
    await event.answer(message="Я вас не понимаю &#128532;\n" \
                               "Пожалуйста, выберите действие на клавиатуре")
