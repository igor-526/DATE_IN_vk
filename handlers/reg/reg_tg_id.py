from vkwave.bots.fsm import StateFilter, NO_STATE, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, Reg
from keyboards import back_keys
from funcs import start_registration, generate_profile_forview, show_menu
from dbase import chk_reg_tg

reg_tg_id_router = DefaultRouter()


@simple_bot_message_handler(reg_tg_id_router, filters.PayloadFilter({"command": "back"}),
                            StateFilter(fsm=fsm, state=Reg.tg_id, for_what=ForWhat.FOR_USER))
async def back(event: SimpleBotEvent):
    await start_registration(event)

@simple_bot_message_handler(reg_tg_id_router,
                            StateFilter(fsm=fsm, state=Reg.tg_id, for_what=ForWhat.FOR_USER))
async def validate(event: SimpleBotEvent):
    # try:
    #     prof = await chk_reg_tg(int(event.text))
    #     if not prof:
    #         raise
    #     if not prof.tg_id:
    #         raise
    #     tg_id = prof.tg_id
    #     mess = await generate_profile_forview(prof.id, 0)
    #     await event.answer(message=mess['msg1'],
    #                        attachment=mess['att1'])
    #     if mess['msg2'] or mess['att2']:
    #         await event.answer(message=mess['msg2'],
    #                            attachment=mess['att2'])
    #     await show_menu(event)
    # except:
    #     await event.answer(message="Не нашёл профиля с таким id\n"
    #                                "Убедись, что вводишь id профиля DATE IN, а не чего-либо другого!",
    #                        keyboard=back_keys.get_keyboard())
    prof = await chk_reg_tg(int(event.text))
    if not prof:
        raise
    if not prof.tg_id:
        raise
    tg_id = prof.tg_id
    mess = await generate_profile_forview(prof.id, 0)
    await event.answer(message=mess['msg1'],
                       attachment=mess['att1'])
    if mess['msg2'] or mess['att2']:
        await event.answer(message=mess['msg2'],
                           attachment=mess['att2'])
    await show_menu(event)