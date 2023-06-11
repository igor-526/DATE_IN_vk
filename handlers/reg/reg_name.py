from vkwave.bots.fsm import StateFilter, NO_STATE, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, Reg
from keyboards import yesnoback_keys
from validators import valid_name
from funcs import start_registration, invalid, f_ask_name_auto, f_ask_name_manual, f_reg_bdate

reg_name_router = DefaultRouter()


@simple_bot_message_handler(reg_name_router, filters.PayloadFilter({"command": "yes"}),
                            StateFilter(fsm=fsm, state=Reg.name_auto, for_what=ForWhat.FOR_USER))
async def reg_bdate(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    name = data['vk']['name']
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'name': name})
    await f_reg_bdate(event)


@simple_bot_message_handler(reg_name_router, filters.PayloadFilter({"command": "no"}),
                            StateFilter(fsm=fsm, state=Reg.name_auto, for_what=ForWhat.FOR_USER))
async def manual(event: SimpleBotEvent):
    await f_ask_name_manual(event)


@simple_bot_message_handler(reg_name_router, filters.PayloadFilter({"command": "back"}),
                            StateFilter(fsm=fsm, state=Reg.name_auto, for_what=ForWhat.FOR_USER))
async def manual(event: SimpleBotEvent):
    await start_registration(event)


@simple_bot_message_handler(reg_name_router,
                            StateFilter(fsm=fsm, state=Reg.name_auto, for_what=ForWhat.FOR_USER))
async def name_invalid(event: SimpleBotEvent):
    await invalid(event, yesnoback_keys)


@simple_bot_message_handler(reg_name_router, filters.PayloadFilter({"command": "back"}),
                            StateFilter(fsm=fsm, state=Reg.name_manual, for_what=ForWhat.FOR_USER))
async def back(event: SimpleBotEvent):
    await f_ask_name_auto(event)


@simple_bot_message_handler(reg_name_router,
                            StateFilter(fsm=fsm, state=Reg.name_manual, for_what=ForWhat.FOR_USER))
async def validation(event: SimpleBotEvent):
    validator = await valid_name(event.text)
    if validator == 'valid':
        await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'name': event.text.capitalize()})
        await f_reg_bdate(event)
    elif validator == 'short':
        return "Имя не может состоять из одного символа\nПопробуй ещё раз!"
    elif validator == 'long':
        return "Не устаёшь писать своё имя?\nПопробуй ещё раз!"
    elif validator == 'invalid':
        return 'Я не верю в такое имя &#128563;\n' \
               'Попробуй ввести ещё раз'
    elif validator == 'obscene':
        return 'И кто же тебя так назвал.. &#128560;\n' \
               'Давай попробуем ещё раз, только нормально &#128514;'
