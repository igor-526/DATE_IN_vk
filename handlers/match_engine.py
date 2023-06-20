from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler, simple_bot_handler
from FSM import fsm, Search, Matches
from keyboards import search_keys
from funcs import search, show_menu, show_new_match, next_old_match, show_old_match, prev_old_match, comp_ask_cat
from vkapi.getidfrommessage import get_id_from_message


match_engine_router = DefaultRouter()


@simple_bot_message_handler(match_engine_router, filters.PayloadFilter({"command": "menu"}),
                            StateFilter(fsm=fsm, state=Matches.new_matches, for_what=ForWhat.FOR_USER))
async def go_menu(event: SimpleBotEvent):
    await show_menu(event)


@simple_bot_message_handler(match_engine_router, filters.PayloadFilter({"command": "search"}),
                            StateFilter(fsm=fsm, state=Matches.new_matches, for_what=ForWhat.FOR_USER))
async def searching(event: SimpleBotEvent):
    await fsm.set_state(state=Search.searching, for_what=ForWhat.FOR_USER, event=event)
    await event.answer(message="Уже ищу..",
                       keyboard=search_keys.get_keyboard())
    await search(event)


@simple_bot_message_handler(match_engine_router, filters.PayloadFilter({"command": "menu"}),
                            StateFilter(fsm=fsm, state=Matches.old_matches, for_what=ForWhat.FOR_USER))
async def go_menu(event: SimpleBotEvent):
    await show_menu(event)


@simple_bot_message_handler(match_engine_router, filters.PayloadFilter({"command": "search"}),
                            StateFilter(fsm=fsm, state=Matches.old_matches, for_what=ForWhat.FOR_USER))
async def searching(event: SimpleBotEvent):
    await fsm.set_state(state=Search.searching, for_what=ForWhat.FOR_USER, event=event)
    await event.answer(message="Уже ищу..",
                       keyboard=search_keys.get_keyboard())
    await search(event)


@simple_bot_message_handler(match_engine_router, filters.PayloadFilter({"command": "next"}),
                            StateFilter(fsm=fsm, state=Matches.new_matches, for_what=ForWhat.FOR_USER))
async def next_new(event: SimpleBotEvent):
    await show_new_match(event)


@simple_bot_message_handler(match_engine_router, filters.PayloadFilter({"command": "showed"}),
                            StateFilter(fsm=fsm, state=Matches.new_matches, for_what=ForWhat.FOR_USER))
async def old(event: SimpleBotEvent):
    await show_old_match(event)


@simple_bot_message_handler(match_engine_router, filters.PayloadFilter({"command": "next"}),
                            StateFilter(fsm=fsm, state=Matches.old_matches, for_what=ForWhat.FOR_USER))
async def next_old(event: SimpleBotEvent):
    await next_old_match(event)


@simple_bot_message_handler(match_engine_router, filters.PayloadFilter({"command": "prev"}),
                            StateFilter(fsm=fsm, state=Matches.old_matches, for_what=ForWhat.FOR_USER))
async def prev_old(event: SimpleBotEvent):
    await prev_old_match(event)


@simple_bot_handler(match_engine_router, None, filters.EventTypeFilter('message_event'),
                    filters.PayloadFilter({'command': 'complaint'}),
                    StateFilter(fsm=fsm, state=Matches.old_matches, for_what=ForWhat.FOR_USER))
async def complaint(event: SimpleBotEvent):
    to_id = await get_id_from_message(event.object.object.conversation_message_id, event.peer_id)
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'compl_to': to_id, 'back_to': 'matches'})
    await comp_ask_cat(event)


@simple_bot_handler(match_engine_router, None, filters.EventTypeFilter('message_event'),
                    filters.PayloadFilter({'command': 'complaint'}),
                    StateFilter(fsm=fsm, state=Matches.new_matches, for_what=ForWhat.FOR_USER))
async def complaint(event: SimpleBotEvent):
    to_id = await get_id_from_message(event.object.object.conversation_message_id, event.peer_id)
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'compl_to': to_id, 'back_to': 'matches'})
    await comp_ask_cat(event)