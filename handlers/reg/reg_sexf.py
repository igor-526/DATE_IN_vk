from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, Reg
from keyboards import sexf_keys
from funcs import f_reg_purposes, f_reg_age_min, invalid

reg_sexf_router = DefaultRouter()


@simple_bot_message_handler(reg_sexf_router, filters.PayloadFilter({"command": "back"}),
                            StateFilter(fsm=fsm, state=Reg.f_sex, for_what=ForWhat.FOR_USER))
async def back(event: SimpleBotEvent):
    await f_reg_purposes(event)


@simple_bot_message_handler(reg_sexf_router, filters.PayloadFilter({"command": "male"}),
                            StateFilter(fsm=fsm, state=Reg.f_sex, for_what=ForWhat.FOR_USER))
async def male(event: SimpleBotEvent):
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'sex_f': [2]})
    await f_reg_age_min(event)


@simple_bot_message_handler(reg_sexf_router, filters.PayloadFilter({"command": "female"}),
                            StateFilter(fsm=fsm, state=Reg.f_sex, for_what=ForWhat.FOR_USER))
async def female(event: SimpleBotEvent):
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'sex_f': [1]})
    await f_reg_age_min(event)


@simple_bot_message_handler(reg_sexf_router, filters.PayloadFilter({"command": "all"}),
                            StateFilter(fsm=fsm, state=Reg.f_sex, for_what=ForWhat.FOR_USER))
async def maleandfemale(event: SimpleBotEvent):
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'sex_f': [1, 2]})
    await f_reg_age_min(event)


@simple_bot_message_handler(reg_sexf_router,
                            StateFilter(fsm=fsm, state=Reg.f_sex, for_what=ForWhat.FOR_USER))
async def do_raise(event: SimpleBotEvent):
    await invalid(event, sexf_keys)