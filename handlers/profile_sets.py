from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import (SimpleBotEvent,
                         DefaultRouter,
                         simple_bot_message_handler,
                         Keyboard)
from FSM import (fsm,
                 ProfileFSM,
                 MenuFSM)
from keyboards import (prof_set_keys,
                       menu_keys,
)
from funcs import gen_profile_settings
from dbase import del_profile

profile_sets_router = DefaultRouter()


@simple_bot_message_handler(profile_sets_router, filters.PayloadFilter({"command": "delete_profile"}),
                            StateFilter(fsm=fsm, state=ProfileFSM.show, for_what=ForWhat.FOR_USER))
async def delete_profile(event: SimpleBotEvent):
    await fsm.set_state(state=ProfileFSM.delete, event=event, for_what=ForWhat.FOR_USER)
    await event.answer(message='Вы действительно хотите удалить свой профиль?\n'
                               'Восстановить его можно будет в течение 2-х суток, после чего профиль будет удалён '
                               'безвозвратно',
                       keyboard=yesno_keys.get_keyboard())


@simple_bot_message_handler(profile_sets_router, filters.PayloadFilter({"command": "yes"}),
                            StateFilter(fsm=fsm, state=ProfileFSM.delete, for_what=ForWhat.FOR_USER))
async def delete_profile_yes(event: SimpleBotEvent):
    await fsm.finish(event=event, for_what=ForWhat.FOR_USER)
    await del_profile(event.user_id)
    await event.answer(message='Профиль удалён. Для восстановления напишите что-нибудь',
                       keyboard=Keyboard.get_empty_keyboard())


@simple_bot_message_handler(profile_sets_router, filters.PayloadFilter({"command": "no"}),
                            StateFilter(fsm=fsm, state=ProfileFSM.delete, for_what=ForWhat.FOR_USER))
async def delete_profile_no(event: SimpleBotEvent):
    await fsm.set_state(state=ProfileFSM.show, event=event, for_what=ForWhat.FOR_USER)
    await event.answer(message='Отменено\nВыберите действие:',
                       keyboard=prof_set_keys.get_keyboard())


@simple_bot_message_handler(profile_sets_router,
                            StateFilter(fsm=fsm, state=ProfileFSM.delete, for_what=ForWhat.FOR_USER))
async def delete_profile_invalid(event: SimpleBotEvent):
    await event.answer(message="Я вас не понимаю &#128532;\n" \
                               "Пожалуйста, выберите действие на клавиатуре",
                       keyboard=yesno_keys.get_keyboard())


@simple_bot_message_handler(profile_sets_router, filters.PayloadFilter({"command": "menu"}),
                            StateFilter(fsm=fsm, state=ProfileFSM.show, for_what=ForWhat.FOR_USER))
async def return_to_menu(event: SimpleBotEvent):
    await fsm.set_state(state=MenuFSM.menu, event=event, for_what=ForWhat.FOR_USER)
    await event.answer(message='Выберите действие:',
                       keyboard=menu_keys.get_keyboard())


@simple_bot_message_handler(profile_sets_router,
                            StateFilter(fsm=fsm, state=ProfileFSM.show, for_what=ForWhat.FOR_USER))
async def profile_invalid(event: SimpleBotEvent):
    await event.answer(message="Я вас не понимаю &#128532;\n" \
                               "Пожалуйста, выберите действие на клавиатуре",
                       keyboard=prof_set_keys.get_keyboard())