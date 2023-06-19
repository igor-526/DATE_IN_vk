from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, Reg
from keyboards import back_keys, yesno_keys, proftg_keys
from funcs import start_registration, generate_profile_forview, show_menu, send_code, invalid
from dbase import chk_reg_tg, add_vk_id

reg_tg_id_router = DefaultRouter()


@simple_bot_message_handler(reg_tg_id_router, filters.PayloadFilter({"command": "back"}),
                            StateFilter(fsm=fsm, state=Reg.tg_id, for_what=ForWhat.FOR_USER))
async def back(event: SimpleBotEvent):
    await start_registration(event)


@simple_bot_message_handler(reg_tg_id_router,
                            StateFilter(fsm=fsm, state=Reg.tg_id, for_what=ForWhat.FOR_USER))
async def validate(event: SimpleBotEvent):
    try:
        prof = await chk_reg_tg(int(event.text))
        if not prof:
            raise
        if not prof.tg_id:
            raise
        tg_id = prof.tg_id
        prof = await generate_profile_forview(prof.id, 0)
        await event.answer(message=prof['msg'],
                           attachment=prof['att'],
                           keyboard=proftg_keys.get_keyboard())
        await event.answer(message='Это твой профиль?',
                           keyboard=yesno_keys.get_keyboard())
        await fsm.set_state(state=Reg.tg_confirm, event=event, for_what=ForWhat.FOR_USER)
        await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'tg_id': tg_id})
    except Exception as exx:
        print(exx)
        await event.answer(message="Не нашёл профиля с таким id\n"
                                   "Убедись, что вводишь id профиля DATE IN, а не чего-либо другого!",
                           attachment='photo28964076_457273215_7115326e569d07ed93',
                           keyboard=back_keys.get_keyboard())


@simple_bot_message_handler(reg_tg_id_router, filters.PayloadFilter({"command": "yes"}),
                            StateFilter(fsm=fsm, state=Reg.tg_confirm, for_what=ForWhat.FOR_USER))
async def conf_yes(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    await send_code(event, data['tg_id'])


@simple_bot_message_handler(reg_tg_id_router, filters.PayloadFilter({"command": "no"}),
                            StateFilter(fsm=fsm, state=Reg.tg_confirm, for_what=ForWhat.FOR_USER))
async def conf_no(event: SimpleBotEvent):
    await start_registration(event)


@simple_bot_message_handler(reg_tg_id_router,
                            StateFilter(fsm=fsm, state=Reg.tg_confirm, for_what=ForWhat.FOR_USER))
async def conf_invalid(event: SimpleBotEvent):
    await invalid(event, yesno_keys)


@simple_bot_message_handler(reg_tg_id_router, filters.PayloadFilter({"command": "cancel"}),
                            StateFilter(fsm=fsm, state=Reg.tg_code, for_what=ForWhat.FOR_USER))
async def code_cancel(event: SimpleBotEvent):
    await start_registration(event)


@simple_bot_message_handler(reg_tg_id_router, filters.PayloadFilter({"command": "repeat"}),
                            StateFilter(fsm=fsm, state=Reg.tg_code, for_what=ForWhat.FOR_USER))
async def code_repeat(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    await send_code(event, data['tg_id'])


@simple_bot_message_handler(reg_tg_id_router,
                            StateFilter(fsm=fsm, state=Reg.tg_code, for_what=ForWhat.FOR_USER))
async def code_valid(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    if int(event.text) == data['code']:
        await event.answer(message='Успешный вход через Telegram!')
        await add_vk_id(data['tg_id'], event.user_id)
        await show_menu(event)
    else:
        await event.answer(message="Код неверный!\n"
                                   "Попробуй ещё раз")
