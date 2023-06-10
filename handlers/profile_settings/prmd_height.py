from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler, simple_bot_handler
from FSM import fsm, Profile
from keyboards import profile_inline_keys
from dbase import upd_d_height
from vkapi import delete_message
from random import randint

prmd_height_router = DefaultRouter()


@simple_bot_handler(prmd_height_router, None, filters.EventTypeFilter('message_event'),
                    filters.PayloadFilter({'command': 'back'}),
                    StateFilter(fsm=fsm, state=Profile.d_m_height, for_what=ForWhat.FOR_USER))
async def back(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    await delete_message(data['del_msgs'], event.peer_id)
    m = await event.api_ctx.messages.send(message="Какую дополнительную информацию хочешь указать?",
                                          keyboard=profile_inline_keys.get_keyboard(),
                                          peer_id=event.peer_id,
                                          random_id=randint(2000000000, 2147483647))
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'del_msgs': [m]})
    await fsm.set_state(state=Profile.desc_more, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_handler(prmd_height_router, None, filters.EventTypeFilter('message_event'),
                    filters.PayloadFilter({'command': 'clean'}),
                    StateFilter(fsm=fsm, state=Profile.d_m_height, for_what=ForWhat.FOR_USER))
async def clean(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    await upd_d_height(data['pr_id'])
    await delete_message(data['del_msgs'], event.peer_id)
    m = await event.api_ctx.messages.send(message="Очистил!\n"
                                                  "Какую дополнительную информацию хочешь указать?",
                                          keyboard=profile_inline_keys.get_keyboard(),
                                          peer_id=event.peer_id,
                                          random_id=randint(2000000000, 2147483647))
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'del_msgs': [m]})
    await fsm.set_state(state=Profile.desc_more, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(prmd_height_router,
                            StateFilter(fsm=fsm, state=Profile.d_m_height, for_what=ForWhat.FOR_USER))
async def validation(event: SimpleBotEvent):
    try:
        if 120 < int(event.text) < 240:
            data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
            await upd_d_height(data['pr_id'], int(event.text))
            await delete_message(data['del_msgs'], event.peer_id)
            m = await event.answer(message="Записал!\n"
                                           "Какую дополнительную информацию хочешь указать?",
                                   keyboard=profile_inline_keys.get_keyboard())
            await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'del_msgs': [m]})
            await fsm.set_state(state=Profile.desc_more, event=event, for_what=ForWhat.FOR_USER)
        else:
            await event.answer("Я не могу поверить в такой рост")
    except ValueError:
        await event.answer("Пожалуйста, напиши мне только цифру.\n"
                           "Сколько твой рост в сантиметрах?")
