from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, Profile
from keyboards import prof_set_keys, cancel_keys
from validators import valid_bdate
from dbase import upd_bdate
import datetime

prs_bdate_router = DefaultRouter()


@simple_bot_message_handler(prs_bdate_router, filters.PayloadFilter({"command": "cancel"}),
                            StateFilter(fsm=fsm, state=Profile.bdate, for_what=ForWhat.FOR_USER))
async def cancel(event: SimpleBotEvent):
    await event.answer("Выберите действие:",
                       keyboard=prof_set_keys.get_keyboard())
    await fsm.set_state(state=Profile.show, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(prs_bdate_router,
                            StateFilter(fsm=fsm, state=Profile.bdate, for_what=ForWhat.FOR_USER))
async def validation(event: SimpleBotEvent):
    validator = await valid_bdate(event.text)
    if validator == 'valid':
        datelist = event.text.split('.')
        bdate = datetime.date(year=int(datelist[2]), month=int(datelist[1]), day=int(datelist[0]))
        await upd_bdate(event.user_id, bdate)
        await event.answer(message='Поменял успешно!\n'
                                   'Выберите действие:',
                           keyboard=prof_set_keys.get_keyboard())
        await fsm.set_state(state=Profile.show, event=event, for_what=ForWhat.FOR_USER)
    elif validator == 'invalid':
        await event.answer(message='Не смог ничего сделать с этим сообщением\n'
                                   'Пожалуйста, введи дату рождения в формате ДД.ММ.ГГГГ',
                           keyboard=cancel_keys.get_keyboard())
    elif validator == 'interval':
        await event.answer(message='У нас ограничение от 14 до 60 лет :(',
                           keyboard=cancel_keys.get_keyboard())
