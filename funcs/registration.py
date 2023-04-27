from FSM import (fsm,
                 Reg)
from vkwave.bots import (SimpleBotEvent,
                         Keyboard)
from keyboards import (yesno_keys,
                       yesnoback_keys,
                       reg_profile_keys)
from vkwave.bots.fsm import ForWhat
from vkapi import (vkuser_info)

async def start_registration(event: SimpleBotEvent):
    await event.answer(message="Подскажите, у Вас уже есть профиль на сайте или в TG?",
                       keyboard=reg_profile_keys.get_keyboard())
    await fsm.set_state(event=event, state=Reg.profile, for_what=ForWhat.FOR_USER)


async def f_ask_name_auto(event: SimpleBotEvent):
    data = fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    profile_info = data['vk']
    await event.answer(message=f"Тогда начнём &#128521;\n"
                               f"Тебя зовут {profile_info['name']}?",
                       keyboard=yesno_keys.get_keyboard())
    fsm.set_state(state=Reg.name_auto, event=event, for_what=ForWhat.FOR_USER)


async def f_ask_name_manual(event: SimpleBotEvent):
    await event.answer(message=f'Как же тогда тебя зовут? &#128527;',
                       keyboard=Keyboard.get_empty_keyboard())
    fsm.set_state(state=Reg.name_manual, event=event, for_what=ForWhat.FOR_USER)