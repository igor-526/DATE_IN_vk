from FSM import fsm
from vkwave.bots import SimpleBotEvent
from vkwave.bots.fsm import ForWhat
from funcs import generate_profile_forview, show_menu
from dbase import get_search_profile
from keyboards import searchin_keys


async def search(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    pr_id = data['pr_id']
    offer = await get_search_profile(pr_id)
    if offer != 'no_profiles':
        await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'offer': offer['id']})
        prof = await generate_profile_forview(offer['id'], offer['dist'])
        await event.answer(message=prof['msg'],
                           attachment=prof['att'],
                           keyboard=searchin_keys.get_keyboard())
    else:
        await event.answer(message="Никого не нашли для тебя\n"
                                   "Не расстраивайся, попробуй поменять настройки поиска")
        await show_menu(event)