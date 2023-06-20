from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler, simple_bot_handler, CallbackAnswer
from random import randint
from FSM import fsm, Search
from keyboards import search_keys
from funcs import search, show_menu, invalid, generate_profile_description, comp_ask_cat
from dbase import profile_like, profile_pass, get_photos
from vkapi.getidfrommessage import get_id_from_message

search_engine_router = DefaultRouter()


@simple_bot_message_handler(search_engine_router, filters.PayloadFilter({"command": "like"}),
                            StateFilter(fsm=fsm, state=Search.searching, for_what=ForWhat.FOR_USER))
async def like_profile(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    result = await profile_like(data['pr_id'], data['offer'])
    if result == 'liked':
        await search(event)
    elif result == 'match':
        await search(event)
        await event.answer('У тебя новый мэтч!\nПосмотреть контакты можно в меню')
    elif result == 'limit':
        await event.answer('На сегодня с лайками всё &#128532;\n'
                           'Завтра можно будет снова!')


@simple_bot_message_handler(search_engine_router, filters.PayloadFilter({"command": "pass"}),
                            StateFilter(fsm=fsm, state=Search.searching, for_what=ForWhat.FOR_USER))
async def pass_profile(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    await profile_pass(data['pr_id'], data['offer'])
    await search(event)


@simple_bot_message_handler(search_engine_router, filters.PayloadFilter({"command": "menu"}),
                            StateFilter(fsm=fsm, state=Search.searching, for_what=ForWhat.FOR_USER))
async def go_menu(event: SimpleBotEvent):
    await show_menu(event)


@simple_bot_handler(search_engine_router, None, filters.EventTypeFilter('message_event'),
                    filters.PayloadFilter({'command': 'get_photo'}))
async def photos(event: SimpleBotEvent):
    of_id = await get_id_from_message(event.object.object.conversation_message_id, event.peer_id)
    photos = await get_photos(of_id)
    if photos:
        await event.api_ctx.messages.send(user_id=event.user_id,
                                          random_id=randint(-2147483648, 2147483647),
                                          attachment=photos)
    else:
        await event.callback_answer(event_data=CallbackAnswer.show_snackbar(text="У пользователя нет больше фото"))


@simple_bot_handler(search_engine_router, None, filters.EventTypeFilter('message_event'),
                    filters.PayloadFilter({'command': 'get_description'}))
async def description(event: SimpleBotEvent):
    of_id = await get_id_from_message(event.object.object.conversation_message_id, event.peer_id)
    msg = await generate_profile_description(of_id)
    await event.api_ctx.messages.send(user_id=event.user_id,
                                      message=msg,
                                      random_id=randint(-2147483648, 2147483647))


@simple_bot_handler(search_engine_router, None, filters.EventTypeFilter('message_event'),
                    filters.PayloadFilter({'command': 'complaint'}),
                    StateFilter(fsm=fsm, state=Search.searching, for_what=ForWhat.FOR_USER))
async def complaint(event: SimpleBotEvent):
    to_id = await get_id_from_message(event.object.object.conversation_message_id, event.peer_id)
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'compl_to': to_id, 'back_to': 'search'})
    await comp_ask_cat(event)


@simple_bot_message_handler(search_engine_router,
                            StateFilter(fsm=fsm, state=Search.searching, for_what=ForWhat.FOR_USER))
async def invalid_profile(event: SimpleBotEvent):
    await invalid(event, search_keys)


