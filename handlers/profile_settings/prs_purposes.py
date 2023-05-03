from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, Profile
from keyboards import prof_set_keys
from validators import valid_purpose
from dbase import upd_purposes

prs_purposes_router = DefaultRouter()


@simple_bot_message_handler(prs_purposes_router, filters.PayloadFilter({"command": "cancel"}),
                            StateFilter(fsm=fsm, state=Profile.purposes, for_what=ForWhat.FOR_USER))
async def cancel(event: SimpleBotEvent):
    await event.answer("Выберите действие:",
                       keyboard=prof_set_keys.get_keyboard())
    await fsm.set_state(state=Profile.show, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(prs_purposes_router,
                            StateFilter(fsm=fsm, state=Profile.purposes, for_what=ForWhat.FOR_USER))
async def valid(event: SimpleBotEvent):
    validator = await valid_purpose(event.text)
    if validator == 'invalid':
        await event.answer(message='Я так не понял\n'
                                   'Пожалуйста, введите только номера целей, отделяя их запятой или пробелом')
    else:
        await upd_purposes(event.user_id, validator)
        await event.answer(message="Успешно поменял!\n"
                                   "Выберите действие:",
                           keyboard=prof_set_keys.get_keyboard())
        await fsm.set_state(state=Profile.show, event=event, for_what=ForWhat.FOR_USER)
