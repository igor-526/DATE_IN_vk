from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, Profile
from keyboards import cancel_keys, filter_keys
from validators import valid_age
from dbase import upd_age_f

prs_age_f_router = DefaultRouter()


@simple_bot_message_handler(prs_age_f_router, filters.PayloadFilter({"command": "cancel"}),
                            StateFilter(fsm=fsm, state=Profile.age_max, for_what=ForWhat.FOR_USER))
async def cancel(event: SimpleBotEvent):
    await event.answer(message="Выбери фильтр:",
                       keyboard=filter_keys.get_keyboard())
    await fsm.set_state(state=Profile.filters, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(prs_age_f_router, filters.PayloadFilter({"command": "cancel"}),
                            StateFilter(fsm=fsm, state=Profile.age_min, for_what=ForWhat.FOR_USER))
async def cancel(event: SimpleBotEvent):
    await event.answer(message="Выбери фильтр:",
                       keyboard=filter_keys.get_keyboard())
    await fsm.set_state(state=Profile.filters, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(prs_age_f_router,
                            StateFilter(fsm=fsm, state=Profile.age_min, for_what=ForWhat.FOR_USER))
async def valid_age_min(event: SimpleBotEvent):
    validator = await valid_age(event.text, None)
    if validator == 'valid':
        await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'age_min': int(event.text)})
        await event.answer(message='Отличный выбор! А теперь введи максимальный возраст для поиска!',
                           keyboard=cancel_keys.get_keyboard())
        await fsm.set_state(state=Profile.age_max, event=event, for_what=ForWhat.FOR_USER)
    elif validator == 'invalid':
        await event.answer(message='Я так не понимаю\n'
                                   'Просто напиши циферку',
                           keyboard=cancel_keys.get_keyboard())
    elif validator == 'too_small':
        await event.answer(message='У нас ограничение с 14 лет\n'
                                   'Попробуй ввести постарше',
                           keyboard=cancel_keys.get_keyboard())
    elif validator == 'too_old':
        await event.answer(message='Ну тут уже проще будет на кладбище поискать\n'
                                   'Попробуй ввести помладше',
                           keyboard=cancel_keys.get_keyboard())


@simple_bot_message_handler(prs_age_f_router,
                            StateFilter(fsm=fsm, state=Profile.age_max, for_what=ForWhat.FOR_USER))
async def valid_age_max(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    validator = await valid_age(event.text, data['age_min'])
    if validator == 'valid':
        await upd_age_f(event.user_id, data['age_min'], int(event.text))
        await event.answer(message="Настройки поиска обновлены!\n"
                                   "Выбери фильтр:",
                           keyboard=filter_keys.get_keyboard())
        await fsm.set_state(state=Profile.filters, event=event, for_what=ForWhat.FOR_USER)
    elif validator == 'invalid':
        await event.answer(message='Я так не понимаю\n'
                                   'Просто напиши циферку',
                           keyboard=cancel_keys.get_keyboard())
    elif validator == 'more_min':
        await event.answer(message='Максимальный возраст для поиска не может быть меньше минимального\n'
                                   'Попробуй ввести постарше',
                           keyboard=cancel_keys.get_keyboard())
    elif validator == 'too_old':
        await event.answer(message='Ну тут уже проще будет на кладбище поискать\n'
                                   'Попробуй ввести помладше',
                           keyboard=cancel_keys.get_keyboard())
