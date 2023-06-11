from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, Profile, Menu
from keyboards import prof_set_keys
from dbase import upd_geo
from funcs import show_menu

prs_geo_router = DefaultRouter()


@simple_bot_message_handler(prs_geo_router, filters.PayloadFilter({"command": "cancel"}),
                            StateFilter(fsm=fsm, state=Profile.geo, for_what=ForWhat.FOR_USER))
async def cancel(event: SimpleBotEvent):
    await event.answer("Выберите действие:",
                       keyboard=prof_set_keys.get_keyboard())
    await fsm.set_state(state=Profile.show, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(prs_geo_router, filters.PayloadFilter({"command": "cancel"}),
                            StateFilter(fsm=fsm, state=Menu.geo, for_what=ForWhat.FOR_USER))
async def cancelmenu(event: SimpleBotEvent):
    await show_menu(event)


@simple_bot_message_handler(prs_geo_router,
                            StateFilter(fsm=fsm, state=Profile.geo, for_what=ForWhat.FOR_USER))
async def getgeo(event: SimpleBotEvent):
    try:
        geo = event.object.object.message.geo
        data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
        await upd_geo(data['pr_id'], geo)
        await event.answer(message='Успешно обновил!\n'
                                   'Выберите действие:',
                           keyboard=prof_set_keys.get_keyboard())
        await fsm.set_state(state=Profile.show, event=event, for_what=ForWhat.FOR_USER)
    except:
        await event.answer(message='Ничего не смог придумать с этим сообщением\n'
                                   'Пожалуйста, отправь мне геопозицию (можно примерную)')


@simple_bot_message_handler(prs_geo_router,
                            StateFilter(fsm=fsm, state=Menu.geo, for_what=ForWhat.FOR_USER))
async def getgeomenu(event: SimpleBotEvent):
    try:
        geo = event.object.object.message.geo
        data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
        await upd_geo(data['pr_id'], geo)
        await event.answer(message='Успешно обновил!')
        await show_menu(event)
    except:
        await event.answer(message='Ничего не смог придумать с этим сообщением\n'
                                   'Пожалуйста, отправь мне геопозицию (можно примерную)')