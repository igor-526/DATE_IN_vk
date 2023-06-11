from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, Reg
from keyboards import sex_keys
from funcs import invalid, f_reg_bdate, f_reg_geo

reg_sex_router = DefaultRouter()


@simple_bot_message_handler(reg_sex_router, filters.PayloadFilter({"command": "male"}),
                            StateFilter(fsm=fsm, state=Reg.sex_manual, for_what=ForWhat.FOR_USER))
async def set_male(event: SimpleBotEvent):
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'sex': 2})
    await f_reg_geo(event)


@simple_bot_message_handler(reg_sex_router, filters.PayloadFilter({"command": "female"}),
                            StateFilter(fsm=fsm, state=Reg.sex_manual, for_what=ForWhat.FOR_USER))
async def set_female(event: SimpleBotEvent):
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'sex': 1})
    await f_reg_geo(event)


@simple_bot_message_handler(reg_sex_router, filters.PayloadFilter({"command": "back"}),
                            StateFilter(fsm=fsm, state=Reg.sex_manual, for_what=ForWhat.FOR_USER))
async def back(event: SimpleBotEvent):
    await f_reg_bdate(event)


@simple_bot_message_handler(reg_sex_router,
                            StateFilter(fsm=fsm, state=Reg.sex_manual, for_what=ForWhat.FOR_USER))
async def do_raise(event: SimpleBotEvent):
    await invalid(event, keys=sex_keys)