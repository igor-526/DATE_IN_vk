from FSM import (fsm,
                 Complaints)
from vkwave.bots import SimpleBotEvent
from keyboards import cancel_keys, complaint_keys, yesno_keys, search_keys
from vkwave.bots.fsm import ForWhat
from funcs.profile import generate_profile_forview
from funcs.searching import search
from dbase import send_complaint
from random import randint


async def comp_ask_cat(event: SimpleBotEvent):
    await event.api_ctx.messages.send(user_id=event.user_id,
                                      random_id=randint(-2147483648, 2147483647),
                                      message="Вы собираетесь оформить жалобу на профиль\n"
                                              "Выберите категорию жалобы:",
                                      keyboard=complaint_keys.get_keyboard())
    await fsm.set_state(state=Complaints.category, event=event, for_what=ForWhat.FOR_USER)


async def comp_ask_desc(event: SimpleBotEvent):
    await event.api_ctx.messages.send(user_id=event.user_id,
                                      random_id=randint(-2147483648, 2147483647),
                                      message="Опиши, пожалуйста, что произошло. Можно приложить фотографии",
                                      keyboard=cancel_keys.get_keyboard())
    await fsm.set_state(state=Complaints.description, event=event, for_what=ForWhat.FOR_USER)


async def comp_confirm(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    prof = await generate_profile_forview(data['compl_to'])
    msg = prof['msg']
    compl_files = len(data['comp_media'])
    compl_desc = data['comp_description']
    msg += f'\n\nЖалоба: {compl_desc}\n+ принято {compl_files} вложения\nОтправить жалобу?'
    await event.answer(message=msg,
                       attachment=prof['att'],
                       keyboard=yesno_keys.get_keyboard())
    await fsm.set_state(state=Complaints.confirm, event=event, for_what=ForWhat.FOR_USER)


async def comp_send(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    await send_complaint(pr_id=data['pr_id'],
                         to_id=data['compl_to'],
                         cat=data['comp_cat'],
                         description=data['comp_description'],
                         images=data['comp_media'])
    await event.answer(message='Жалоба успешно отправлена',
                       keyboard=search_keys.get_keyboard())
    await search(event)
