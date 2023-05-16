from FSM import (fsm,
                 Menu)
from vkwave.bots import SimpleBotEvent
from keyboards import menu_keys
from vkwave.bots.fsm import ForWhat


async def show_menu(event: SimpleBotEvent):
    await event.answer(message="Выберите действие:",
                       keyboard=menu_keys.get_keyboard())
    await fsm.set_state(state=Menu.menu, event=event, for_what=ForWhat.FOR_USER)


async def menu_invalid(event: SimpleBotEvent):
    await event.answer(message="Я могу понять только нажатие кнопки на клавиатуре\n"
                               "Пожалуйста, выберите действие:",
                       keyboard=menu_keys.get_keyboard())