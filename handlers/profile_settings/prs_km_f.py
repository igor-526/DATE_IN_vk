from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, Profile
from keyboards import cancel_keys, filter_keys
from dbase import upd_dist

prs_km_f_router = DefaultRouter()


@simple_bot_message_handler(prs_km_f_router, filters.PayloadFilter({"command": "cancel"}),
                            StateFilter(fsm=fsm, state=Profile.km_f, for_what=ForWhat.FOR_USER))
async def cancel(event: SimpleBotEvent):
    await event.answer(message="Выбери фильтр:",
                       keyboard=filter_keys.get_keyboard())
    await fsm.set_state(state=Profile.filters, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(prs_km_f_router,
                            StateFilter(fsm=fsm, state=Profile.km_f, for_what=ForWhat.FOR_USER))
async def validation(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    try:
        dist = int(event.text)
        if dist < 5:
            await event.answer(message="Это слишком мало, мне пока что будет сложно найти профили так близко\n"
                                       "Минимум 5 км",
                               keyboard=cancel_keys.get_keyboard())
        elif dist > 60:
            await event.answer(message="Это слишком далеко\n"
                                       "Давай поищем ближе 60км. Если нужен другой город, просто обнови геолокацию",
                               keyboard=cancel_keys.get_keyboard())
        else:
            await upd_dist(data['pr_id'], dist)
            await event.answer(message="Успешно обновил!\n"
                                       "Выбери фильтр:",
                               keyboard=filter_keys.get_keyboard())
            await fsm.set_state(state=Profile.filters, event=event, for_what=ForWhat.FOR_USER)
    except:
        await event.answer(message="Я не знаю, что делать с этим сообщением\n"
                                   "Мне нужна только циферка, в радиусе скольки километров будем искать другие профили",
                           keyboard=cancel_keys.get_keyboard())
