from vkwave.bots.fsm import StateFilter, ForWhat, ANY_STATE
from vkwave.bots import Keyboard
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, Menu
from dbase import get_profile_id, chk_reg
from funcs import show_menu
from keyboards import cancel_keys

commands_router = DefaultRouter()


@simple_bot_message_handler(commands_router, filters.CommandsFilter('report'),
                            StateFilter(fsm=fsm, state=ANY_STATE, for_what=ForWhat.FOR_USER))
async def report(event: SimpleBotEvent):
    pr_id = await get_profile_id(event.user_id)
    await event.answer("Напишите своё сообщение (Или несколько сообщений) для администрации\n"
                       "Можно отправить фото (или несколько фото) отделными сообщениями. После чего нажми 'Готово!'",
                       keyboard=cancel_keys.get_keyboard())
    await fsm.set_state(event=event, for_what=ForWhat.FOR_USER, state=Menu.report)
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'pr_id': pr_id})


@simple_bot_message_handler(commands_router, filters.CommandsFilter('rules'),
                            StateFilter(fsm=fsm, state=ANY_STATE, for_what=ForWhat.FOR_USER))
async def rules(event: SimpleBotEvent):
    with open(file='fixtures/rules.txt', mode='r') as file:
        await event.answer(message=file.read())


@simple_bot_message_handler(commands_router, filters.CommandsFilter('reset'),
                            StateFilter(fsm=fsm, state=ANY_STATE, for_what=ForWhat.FOR_USER))
async def reset(event: SimpleBotEvent):
    await fsm.finish(event=event, for_what=ForWhat.FOR_USER)
    await event.answer("Успешно. Напишите что-нибудь",
                       keyboard=Keyboard.get_empty_keyboard())


@simple_bot_message_handler(commands_router, filters.CommandsFilter('menu'),
                            StateFilter(fsm=fsm, state=ANY_STATE, for_what=ForWhat.FOR_USER))
async def smenu(event: SimpleBotEvent):
    check = await chk_reg(event.user_id)
    if check:
        if check.status == 'active':
            await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'pr_id': check.id})
            await show_menu(event)
        elif check.status == 'deactivated':
            await event.answer(message="Ошибка\n"
                                       "Ваш профиль дактивирован, команда недоступна")
        elif check.status == 'freeze':
            await event.answer(message='Ваш профиль был временно заморожен администрацией, так как нарушал правила '
                                       'использования сервиса\n'
                                       'Если Вы с этим не согласны, напишите в /report')


@simple_bot_message_handler(commands_router, filters.CommandsFilter('help'),
                            StateFilter(fsm=fsm, state=ANY_STATE, for_what=ForWhat.FOR_USER))
async def gethelp(event: SimpleBotEvent):
    with open(file='fixtures/help.txt', mode='r') as file:
        await event.answer(message=file.read())
