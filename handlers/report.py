from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, Menu
from keyboards import yesno_keys
from funcs import comp_confirm, show_menu, invalid
from vkapi import get_message
from dbase import send_complaint

report_router = DefaultRouter()


@simple_bot_message_handler(report_router, filters.PayloadFilter({"command": "cancel"}),
                            StateFilter(fsm=fsm, state=Menu.report, for_what=ForWhat.FOR_USER))
async def cancel(event: SimpleBotEvent):
    await event.answer("Репорт отменён")
    await show_menu(event)


@simple_bot_message_handler(report_router, filters.PayloadFilter({"command": "no"}),
                            StateFilter(fsm=fsm, state=Menu.report_confirm, for_what=ForWhat.FOR_USER))
async def cancel(event: SimpleBotEvent):
    await event.answer("Репорт отменён")
    await show_menu(event)


@simple_bot_message_handler(report_router,
                            StateFilter(fsm=fsm, state=Menu.report, for_what=ForWhat.FOR_USER))
async def description(event: SimpleBotEvent):
    info = await get_message(event.object.object.message.id)
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={
        'comp_media': info['photos'], 'comp_description': info['text']})
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    await event.answer(f'{data["comp_description"]}\n'
                       f'+ {len(data["comp_media"])} вложений\n'
                       f'Всё верно?',
                       keyboard=yesno_keys.get_keyboard())
    await fsm.set_state(state=Menu.report_confirm, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(report_router, filters.PayloadFilter({"command": "yes"}),
                            StateFilter(fsm=fsm, state=Menu.report_confirm, for_what=ForWhat.FOR_USER))
async def confirm(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    await send_complaint(data['pr_id'], None, 'report', data['comp_description'], data['comp_media'])
    await event.answer("Репорт успешно отправлен!")
    await show_menu(event)


@simple_bot_message_handler(report_router,
                            StateFilter(fsm=fsm, state=Menu.report_confirm, for_what=ForWhat.FOR_USER))
async def inv(event: SimpleBotEvent):
    await invalid(event, yesno_keys)