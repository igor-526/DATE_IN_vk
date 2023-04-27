from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, Reg
from keyboards import back_keys
from funcs import f_reg_description, f_reg_sexf
from validators import valid_purpose

reg_purposes_router = DefaultRouter()


@simple_bot_message_handler(reg_purposes_router, filters.PayloadFilter({"command": "back"}),
                            StateFilter(fsm=fsm, state=Reg.purposes, for_what=ForWhat.FOR_USER))
async def back(event: SimpleBotEvent):
    await f_reg_description(event)


@simple_bot_message_handler(reg_purposes_router,
                            StateFilter(fsm=fsm, state=Reg.purposes, for_what=ForWhat.FOR_USER))
async def valid(event: SimpleBotEvent):
    validator = await valid_purpose(event.text)
    if validator == 'invalid':
        await event.answer(message='Я так не понял\n'
                                   'Пожалуйста, введите только номера целей, отделяя их запятой или пробелом',
                           keyboard=back_keys.get_keyboard())
    else:
        await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'purposes': validator})
        await f_reg_sexf(event)
