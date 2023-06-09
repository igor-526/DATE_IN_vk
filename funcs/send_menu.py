from FSM import (fsm,
                 Menu)
from vkwave.bots import SimpleBotEvent
from keyboards import menu_keys
from vkwave.bots.fsm import ForWhat
from dbase import get_profile_id


async def show_menu(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    if data:
        try:
            keyss = await menu_keys(data.get('pr_id'))
            await event.answer(message="Выберите действие:",
                               keyboard=keyss.get_keyboard())
            await fsm.set_state(state=Menu.menu, event=event, for_what=ForWhat.FOR_USER)
        except:
            pass
    else:
        try:
            pr_id = await get_profile_id(event.user_id)
            keyss = await menu_keys(pr_id)
            await event.answer(message="Выберите действие:",
                               keyboard=keyss.get_keyboard())
            await fsm.set_state(state=Menu.menu, event=event, for_what=ForWhat.FOR_USER)
        except:
            await event.answer(message="Ошибка. Профиль не зарегистрирован")


async def menu_invalid(event: SimpleBotEvent):
    await event.answer(message="Я могу понять только нажатие кнопки на клавиатуре\n"
                               "Пожалуйста, выбери действие:")
