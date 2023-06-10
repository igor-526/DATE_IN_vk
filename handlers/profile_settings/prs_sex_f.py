from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, Profile
from keyboards import filter_keys
from dbase import upd_sex_f

prs_sex_f_router = DefaultRouter()


@simple_bot_message_handler(prs_sex_f_router, filters.PayloadFilter({"command": "back"}),
                            StateFilter(fsm=fsm, state=Profile.sex_f, for_what=ForWhat.FOR_USER))
async def cancel(event: SimpleBotEvent):
    await event.answer(message="Выбери фильтр:",
                       keyboard=filter_keys.get_keyboard())
    await fsm.set_state(state=Profile.filters, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(prs_sex_f_router, filters.PayloadFilter({"command": "male"}),
                            StateFilter(fsm=fsm, state=Profile.sex_f, for_what=ForWhat.FOR_USER))
async def male(event: SimpleBotEvent):
    await upd_sex_f(event.user_id, [2])
    await event.answer(message="Настройки поиска обновлены\n"
                               "Выбери фильтр:",
                       keyboard=filter_keys.get_keyboard())
    await fsm.set_state(state=Profile.filters, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(prs_sex_f_router, filters.PayloadFilter({"command": "female"}),
                            StateFilter(fsm=fsm, state=Profile.sex_f, for_what=ForWhat.FOR_USER))
async def female(event: SimpleBotEvent):
    await upd_sex_f(event.user_id, [1])
    await event.answer(message="Настройки поиска обновлены\n"
                               "Выбери фильтр:",
                       keyboard=filter_keys.get_keyboard())
    await fsm.set_state(state=Profile.filters, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(prs_sex_f_router, filters.PayloadFilter({"command": "all"}),
                            StateFilter(fsm=fsm, state=Profile.sex_f, for_what=ForWhat.FOR_USER))
async def maleandfemale(event: SimpleBotEvent):
    await upd_sex_f(event.user_id, [1, 2])
    await event.answer(message="Настройки поиска обновлены\n"
                               "Выбери фильтр:",
                       keyboard=filter_keys.get_keyboard())
    await fsm.set_state(state=Profile.filters, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(prs_sex_f_router,
                            StateFilter(fsm=fsm, state=Profile.sex_f, for_what=ForWhat.FOR_USER))
async def invalid(event: SimpleBotEvent):
    await event.answer(message="Я не понимаю &#128532;\n"
                               "Пожалуйста, выбери действие на клавиатуре")
