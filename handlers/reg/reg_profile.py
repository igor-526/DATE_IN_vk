from vkwave.bots.fsm import StateFilter, NO_STATE, ForWhat, ANY_STATE
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, Reg
from keyboards import reg_profile_keys, back_keys
from vkapi import vkuser_info
from funcs import start_registration, invalid, f_ask_name_auto

reg_profile_router = DefaultRouter()


@simple_bot_message_handler(reg_profile_router, filters.CommandsFilter('reset'),
                            StateFilter(fsm=fsm, state=ANY_STATE, for_what=ForWhat.FOR_USER))
async def reset(event: SimpleBotEvent):
    await fsm.finish(event=event, for_what=ForWhat.FOR_USER)
    await event.answer(message='FSM сброшена\nНапиши любое сообщение')


@simple_bot_message_handler(reg_profile_router, filters.PayloadFilter({"command": "registration"}),
                            StateFilter(fsm=fsm, state=NO_STATE, for_what=ForWhat.FOR_USER))
async def registration(event: SimpleBotEvent):
    await start_registration(event)


@simple_bot_message_handler(reg_profile_router, filters.PayloadFilter({"command": "none"}),
                            StateFilter(fsm=fsm, state=Reg.profile, for_what=ForWhat.FOR_USER))
async def no_profile(event: SimpleBotEvent):
    vk_data = await vkuser_info(event.user_id)
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'vk': vk_data})
    await f_ask_name_auto(event)


@simple_bot_message_handler(reg_profile_router, filters.PayloadFilter({"command": "tg"}),
                            StateFilter(fsm=fsm, state=Reg.profile, for_what=ForWhat.FOR_USER))
async def telegram(event: SimpleBotEvent):
    await event.answer(message="Пожалуйста, напиши мне id своего профиля\n"
                               "Узнать его можно в настройках профиля",
                       attachment='photo28964076_457273215_7115326e569d07ed93',
                       keyboard=back_keys.get_keyboard())
    await fsm.set_state(state=Reg.tg_id, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(reg_profile_router, filters.PayloadFilter({"command": "site"}),
                            StateFilter(fsm=fsm, state=Reg.profile, for_what=ForWhat.FOR_USER))
async def telegram(event: SimpleBotEvent):
    await invalid(event, reg_profile_keys)


@simple_bot_message_handler(reg_profile_router,
                            StateFilter(fsm=fsm, state=Reg.profile, for_what=ForWhat.FOR_USER))
async def f_invalid(event: SimpleBotEvent):
    await invalid(event, reg_profile_keys)
