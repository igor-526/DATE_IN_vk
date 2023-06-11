from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, Reg
from keyboards import yesnoback_keys, back_keys
from validators import valid_bdate, valid_year
from funcs import invalid, f_ask_name_auto, f_reg_sex, f_reg_bdate_manual

reg_bdate_router = DefaultRouter()


@simple_bot_message_handler(reg_bdate_router, filters.PayloadFilter({"command": "yes"}),
                            StateFilter(fsm=fsm, state=Reg.bdate_auto, for_what=ForWhat.FOR_USER))
async def confirm(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    bdate = data['vk']['bdate']
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'bdate': bdate})
    await f_reg_sex(event)


@simple_bot_message_handler(reg_bdate_router, filters.PayloadFilter({"command": "no"}),
                            StateFilter(fsm=fsm, state=Reg.bdate_auto, for_what=ForWhat.FOR_USER))
async def manual(event: SimpleBotEvent):
    await f_reg_bdate_manual(event)


@simple_bot_message_handler(reg_bdate_router, filters.PayloadFilter({"command": "back"}),
                            StateFilter(fsm=fsm, state=Reg.bdate_auto, for_what=ForWhat.FOR_USER))
async def backto_name(event: SimpleBotEvent):
    await f_ask_name_auto(event)


@simple_bot_message_handler(reg_bdate_router,
                            StateFilter(fsm=fsm, state=Reg.bdate_auto, for_what=ForWhat.FOR_USER))
async def do_raise(event: SimpleBotEvent):
    await invalid(event, keys=yesnoback_keys)


@simple_bot_message_handler(reg_bdate_router, filters.PayloadFilter({"command": "back"}),
                            StateFilter(fsm=fsm, state=Reg.bdate_year, for_what=ForWhat.FOR_USER))
async def backto_name(event: SimpleBotEvent):
    await f_ask_name_auto(event)


@simple_bot_message_handler(reg_bdate_router,
                            StateFilter(fsm=fsm, state=Reg.bdate_year, for_what=ForWhat.FOR_USER))
async def val_year(event: SimpleBotEvent):
    validator = await valid_year(event.text)
    if validator == 'valid':
        data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
        bdate = data['vk']['bdate']+'.'+ event.text
        await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'bdate': bdate})
        await f_reg_sex(event)
    elif validator == 'invalid':
        await event.answer(message='Не смог ничего сделать с этим сообщением\n'
                                   'Пожалуйста, введи год своего рождения полностью',
                           keyboard=back_keys.get_keyboard())


@simple_bot_message_handler(reg_bdate_router, filters.PayloadFilter({"command": "back"}),
                            StateFilter(fsm=fsm, state=Reg.bdate_manual, for_what=ForWhat.FOR_USER))
async def back_toname(event: SimpleBotEvent):
    await f_ask_name_auto(event)


@simple_bot_message_handler(reg_bdate_router,
                            StateFilter(fsm=fsm, state=Reg.bdate_manual, for_what=ForWhat.FOR_USER))
async def val_bdate(event: SimpleBotEvent):
    validator = await valid_bdate(event.text)
    if validator == 'valid':
        bdate = event.text
        await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'bdate': bdate})
        await f_reg_sex(event)
    elif validator == 'invalid':
        await event.answer(message='Не смог ничего сделать с этим сообщением\n'
                                   'Пожалуйста, введи дату рождения в формате ДД.ММ.ГГГГ',
                           keyboard=back_keys.get_keyboard())
    elif validator == 'interval':
        await event.answer(message='У нас ограничение от 14 до 60 лет :(',
                           keyboard=back_keys.get_keyboard())
