from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler, simple_bot_handler
from vkwave.types.bot_events import BotEventType
from bot import bot
from FSM import fsm, Search
from keyboards import search_keys
from funcs import search, show_menu, invalid
from dbase import profile_like, profile_pass

search_engine_router = DefaultRouter()


@simple_bot_message_handler(search_engine_router, filters.PayloadFilter({"command": "like"}),
                            StateFilter(fsm=fsm, state=Search.searching, for_what=ForWhat.FOR_USER))
async def like_profile(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    await profile_like(data['id'], data['offer'])
    await search(event)


@simple_bot_message_handler(search_engine_router, filters.PayloadFilter({"command": "pass"}),
                            StateFilter(fsm=fsm, state=Search.searching, for_what=ForWhat.FOR_USER))
async def pass_profile(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    await profile_pass(data['id'], data['offer'])
    await search(event)




@simple_bot_message_handler(search_engine_router, filters.PayloadFilter({"command": "menu"}),
                            StateFilter(fsm=fsm, state=Search.searching, for_what=ForWhat.FOR_USER))
async def go_menu(event: SimpleBotEvent):
    await show_menu(event)


@simple_bot_handler(search_engine_router, filters.EventTypeFilter("message_event"),
                    StateFilter(fsm=fsm, state=Search.searching, for_what=ForWhat.FOR_USER))
async def bbb(event: SimpleBotEvent):
    print(event)


@simple_bot_message_handler(search_engine_router,
                            StateFilter(fsm=fsm, state=Search.searching, for_what=ForWhat.FOR_USER))
async def invalid_profile(event: SimpleBotEvent):
    await invalid(event, search_keys)
