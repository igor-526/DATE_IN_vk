from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler, simple_bot_handler
from FSM import fsm, Profile
from keyboards import profile_inline_keys
from dbase import upd_d_busy
from vkapi import delete_message
from random import randint

prmd_busy_router = DefaultRouter()


@simple_bot_handler(prmd_busy_router, None, filters.EventTypeFilter('message_event'),
                    filters.PayloadFilter({'command': 'back'}),
                    StateFilter(fsm=fsm, state=Profile.d_m_busy, for_what=ForWhat.FOR_USER))
async def back(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    await delete_message(data['del_msgs'], event.peer_id)
    m = await event.api_ctx.messages.send(message="Какую дополнительную информацию хочешь указать?",
                                          keyboard=profile_inline_keys.get_keyboard(),
                                          peer_id=event.peer_id,
                                          random_id=randint(2000000000, 2147483647))
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'del_msgs': [m]})
    await fsm.set_state(state=Profile.desc_more, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_handler(prmd_busy_router, None, filters.EventTypeFilter('message_event'),
                    filters.PayloadFilter({'command': 'clean'}),
                    StateFilter(fsm=fsm, state=Profile.d_m_busy, for_what=ForWhat.FOR_USER))
async def clean(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    await upd_d_busy(data['pr_id'])
    await delete_message(data['del_msgs'], event.peer_id)
    m = await event.api_ctx.messages.send(message="Очистил!\n"
                                                  "Какую дополнительную информацию хочешь указать?",
                                          keyboard=profile_inline_keys.get_keyboard(),
                                          peer_id=event.peer_id,
                                          random_id=randint(2000000000, 2147483647))
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'del_msgs': [m]})
    await fsm.set_state(state=Profile.desc_more, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_handler(prmd_busy_router, None, filters.EventTypeFilter('message_event'),
                    filters.PayloadFilter({'command': 'none'}),
                    StateFilter(fsm=fsm, state=Profile.d_m_busy, for_what=ForWhat.FOR_USER))
async def no(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    await upd_d_busy(data['pr_id'], "не учусь и не работаю")
    m = await event.api_ctx.messages.send(message="Записал!\n"
                                                  "Какую дополнительную информацию хочешь указать?",
                                          keyboard=profile_inline_keys.get_keyboard(),
                                          peer_id=event.peer_id,
                                          random_id=randint(2000000000, 2147483647))
    await delete_message(data['del_msgs'], event.peer_id)
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'del_msgs': [m]})
    await fsm.set_state(state=Profile.desc_more, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_handler(prmd_busy_router, None, filters.EventTypeFilter('message_event'),
                    filters.PayloadFilter({'command': 'learning'}),
                    StateFilter(fsm=fsm, state=Profile.d_m_busy, for_what=ForWhat.FOR_USER))
async def learning(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    await upd_d_busy(data['pr_id'], "только учусь")
    m = await event.api_ctx.messages.send(message="Записал!\n"
                                                  "Какую дополнительную информацию хочешь указать?",
                                          keyboard=profile_inline_keys.get_keyboard(),
                                          peer_id=event.peer_id,
                                          random_id=randint(2000000000, 2147483647))
    await delete_message(data['del_msgs'], event.peer_id)
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'del_msgs': [m]})
    await fsm.set_state(state=Profile.desc_more, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_handler(prmd_busy_router, None, filters.EventTypeFilter('message_event'),
                    filters.PayloadFilter({'command': 'working'}),
                    StateFilter(fsm=fsm, state=Profile.d_m_busy, for_what=ForWhat.FOR_USER))
async def working(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    await upd_d_busy(data['pr_id'], "только работаю")
    m = await event.api_ctx.messages.send(message="Записал!\n"
                                                  "Какую дополнительную информацию хочешь указать?",
                                          keyboard=profile_inline_keys.get_keyboard(),
                                          peer_id=event.peer_id,
                                          random_id=randint(2000000000, 2147483647))
    await delete_message(data['del_msgs'], event.peer_id)
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'del_msgs': [m]})
    await fsm.set_state(state=Profile.desc_more, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_handler(prmd_busy_router, None, filters.EventTypeFilter('message_event'),
                    filters.PayloadFilter({'command': 'and'}),
                    StateFilter(fsm=fsm, state=Profile.d_m_busy, for_what=ForWhat.FOR_USER))
async def landw(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    await upd_d_busy(data['pr_id'], "учусь и работаю")
    m = await event.api_ctx.messages.send(message="Записал!\n"
                                                  "Какую дополнительную информацию хочешь указать?",
                                          keyboard=profile_inline_keys.get_keyboard(),
                                          peer_id=event.peer_id,
                                          random_id=randint(2000000000, 2147483647))
    await delete_message(data['del_msgs'], event.peer_id)
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'del_msgs': [m]})
    await fsm.set_state(state=Profile.desc_more, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(prmd_busy_router,
                            StateFilter(fsm=fsm, state=Profile.d_m_busy, for_what=ForWhat.FOR_USER))
async def invalid(event: SimpleBotEvent):
    await event.answer("Я не понимаю &#128532;\n"
                       "Пожалуйста, выбери действие на клавиатуре")
