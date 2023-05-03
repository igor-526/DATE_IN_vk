from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler, Keyboard
from FSM import fsm, Profile
from keyboards import prof_set_keys
from dbase import upd_deactivate_profile
import datetime

prs_deactivate_router = DefaultRouter()


@simple_bot_message_handler(prs_deactivate_router, filters.PayloadFilter({"command": "yes"}),
                            StateFilter(fsm=fsm, state=Profile.delete, for_what=ForWhat.FOR_USER))
async def deactivate(event: SimpleBotEvent):
    await upd_deactivate_profile(event.user_id)
    deletetime = datetime.datetime.now() + datetime.timedelta(days=7)
    await fsm.finish(event=event, for_what=ForWhat.FOR_USER)
    await event.answer(message=f'Профиль деактивирован\n'
                               f'{deletetime.strftime("%d.%m %H:%M")} будет удалён окончательно\n'
                               f'До этого момента можно будет только восстановить',
                       keyboard=Keyboard.get_empty_keyboard())


@simple_bot_message_handler(prs_deactivate_router, filters.PayloadFilter({"command": "no"}),
                            StateFilter(fsm=fsm, state=Profile.delete, for_what=ForWhat.FOR_USER))
async def cancel(event: SimpleBotEvent):
    await event.answer(message='Фух! Я уж испугался!\n'
                               'Выберите действие:',
                       keyboard=prof_set_keys.get_keyboard())
    await fsm.set_state(state=Profile.show, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(prs_deactivate_router,
                            StateFilter(fsm=fsm, state=Profile.delete, for_what=ForWhat.FOR_USER))
async def invalid(event: SimpleBotEvent):
    await event.answer(message="Я вас не понимаю &#128532;\n"
                               "Пожалуйста, выберите действие на клавиатуре")