from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, Reg
from keyboards import back_keys
from funcs import f_reg_sexf, f_reg_age_max
from validators import valid_age

reg_age_min_router = DefaultRouter()


@simple_bot_message_handler(reg_age_min_router, filters.PayloadFilter({"command": "back"}),
                            StateFilter(fsm=fsm, state=Reg.f_age_min, for_what=ForWhat.FOR_USER))
async def back(event: SimpleBotEvent):
    await f_reg_sexf(event)


@simple_bot_message_handler(reg_age_min_router,
                            StateFilter(fsm=fsm, state=Reg.f_age_min, for_what=ForWhat.FOR_USER))
async def valid(event: SimpleBotEvent):
    validator = await valid_age(event.text, None)
    if validator == 'valid':
        await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'age_min': int(event.text)})
        await f_reg_age_max(event)
    elif validator == 'invalid':
        await event.answer(message='Я так не понимаю\n'
                                   'Просто напиши циферку',
                           keyboard=back_keys.get_keyboard())
    elif validator == 'too_small':
        await event.answer(message='У нас ограничение с 14 лет\n'
                                   'Попробуй ввести постарше',
                           keyboard=back_keys.get_keyboard())
    elif validator == 'too_old':
        await event.answer(message='Ну тут уже проще будет на кладбище поискать\n'
                                   'Попробуй ввести помладше',
                           keyboard=back_keys.get_keyboard())