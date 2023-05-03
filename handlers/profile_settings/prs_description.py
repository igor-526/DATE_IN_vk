from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, Profile
from keyboards import prof_set_keys
from validators import valid_description
from dbase import upd_description

prs_description_router = DefaultRouter()


@simple_bot_message_handler(prs_description_router, filters.PayloadFilter({"command": "cancel"}),
                            StateFilter(fsm=fsm, state=Profile.description, for_what=ForWhat.FOR_USER))
async def cancel(event: SimpleBotEvent):
    await event.answer("Выберите действие:",
                       keyboard=prof_set_keys.get_keyboard())
    await fsm.set_state(state=Profile.show, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(prs_description_router,
                            StateFilter(fsm=fsm, state=Profile.description, for_what=ForWhat.FOR_USER))
async def valid(event: SimpleBotEvent):
    validator = await valid_description(event.text)
    if validator == 'valid':
        await upd_description(event.user_id, event.text)
        await event.answer(message='Описание успешно обновлено!\n'
                                   'Выберите действие:',
                           keyboard=prof_set_keys.get_keyboard())
        await fsm.set_state(state=Profile.show, event=event, for_what=ForWhat.FOR_USER)
    elif validator == 'obscene':
        return "Мы против нецензурной лексики\n" \
               "Попробуй переписать так, чтобы её там не было"
    elif validator == 'long':
        return "Слишком длинное описание\n" \
               "К сожалению, это не наше ограничение, а мессенджеров"
