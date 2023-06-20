from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, Complaints, Search
from keyboards import search_keys, newmatch_keys
from funcs import show_new_match, comp_confirm
from vkapi import get_message

comp_desc_router = DefaultRouter()


@simple_bot_message_handler(comp_desc_router, filters.PayloadFilter({"command": "cancel"}),
                            StateFilter(fsm=fsm, state=Complaints.description, for_what=ForWhat.FOR_USER))
async def cancel(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    if data['back_to'] == 'search':
        await fsm.set_state(state=Search.searching, event=event, for_what=ForWhat.FOR_USER)
        await event.answer(message="Жалоба отменена",
                           keyboard=search_keys.get_keyboard())
    elif data['back_to'] == 'matches':
        await event.answer(message="Жалоба отменена",
                           keyboard=newmatch_keys.get_keyboard())
        await show_new_match(event)


@simple_bot_message_handler(comp_desc_router,
                            StateFilter(fsm=fsm, state=Complaints.description, for_what=ForWhat.FOR_USER))
async def description(event: SimpleBotEvent):
    info = await get_message(event.object.object.message.id)
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={
        'comp_media': info['photos'], 'comp_description': info['text']})
    await comp_confirm(event)
