from vkwave.bots.fsm import StateFilter, ForWhat, ANY_STATE
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm
from dbase import upd_delete_profile

commands_router = DefaultRouter()


@simple_bot_message_handler(commands_router, filters.CommandsFilter('del_profile'),
                            StateFilter(fsm=fsm, state=ANY_STATE, for_what=ForWhat.FOR_USER))
async def delete_profile(event: SimpleBotEvent):
    await upd_delete_profile(event.user_id)
    await event.answer('profile was deleted')
