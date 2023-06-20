from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, Complaints, Search
from keyboards import search_keys, newmatch_keys, yesno_keys
from funcs import invalid, show_new_match, comp_send

comp_confirm_router = DefaultRouter()


@simple_bot_message_handler(comp_confirm_router, filters.PayloadFilter({"command": "no"}),
                            StateFilter(fsm=fsm, state=Complaints.confirm, for_what=ForWhat.FOR_USER))
async def no(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    if data['back_to'] == 'search':
        await fsm.set_state(state=Search.searching, event=event, for_what=ForWhat.FOR_USER)
        await event.answer(message="Жалоба отменена",
                           keyboard=search_keys.get_keyboard())
    elif data['back_to'] == 'matches':
        await event.answer(message="Жалоба отменена",
                           keyboard=newmatch_keys.get_keyboard())
        await show_new_match(event)


@simple_bot_message_handler(comp_confirm_router, filters.PayloadFilter({"command": "yes"}),
                            StateFilter(fsm=fsm, state=Complaints.confirm, for_what=ForWhat.FOR_USER))
async def yes(event: SimpleBotEvent):
    await comp_send(event)


@simple_bot_message_handler(comp_confirm_router,
                            StateFilter(fsm=fsm, state=Complaints.confirm, for_what=ForWhat.FOR_USER))
async def inv(event: SimpleBotEvent):
    await invalid(event, yesno_keys)