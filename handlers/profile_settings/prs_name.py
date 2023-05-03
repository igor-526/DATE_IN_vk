from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, Profile
from keyboards import prof_set_keys
from validators import valid_name
from dbase import upd_name

prs_name_router = DefaultRouter()


@simple_bot_message_handler(prs_name_router, filters.PayloadFilter({"command": "cancel"}),
                            StateFilter(fsm=fsm, state=Profile.name, for_what=ForWhat.FOR_USER))
async def cancel(event: SimpleBotEvent):
    await event.answer("Выберите действие:",
                       keyboard=prof_set_keys.get_keyboard())
    await fsm.set_state(state=Profile.show, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(prs_name_router,
                            StateFilter(fsm=fsm, state=Profile.name, for_what=ForWhat.FOR_USER))
async def validation(event: SimpleBotEvent):
    validator = await valid_name(event.text)
    if validator == 'valid':
        await upd_name(event.user_id, event.text)
        await event.answer(message="Успешно!\n"
                                   "Выберите действие:",
                           keyboard=prof_set_keys.get_keyboard())
        await fsm.set_state(state=Profile.show, event=event, for_what=ForWhat.FOR_USER)
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
