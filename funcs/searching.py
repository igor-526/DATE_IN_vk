from FSM import fsm
from vkwave.bots import SimpleBotEvent
from vkwave.bots.fsm import ForWhat
from funcs import generate_profile_forview, show_menu
from dbase import get_profile_id, get_search_profile
from keyboards import search_in_keys


async def search(event: SimpleBotEvent):
    pr_id = await get_profile_id(event.user_id)
    offer = await get_search_profile(pr_id)
    if offer != 'no_profiles':
        await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'id': pr_id, 'offer': offer['id']})
        prof = await generate_profile_forview(offer['id'], offer['dist'])
        await event.answer(message=prof['msg1'],
                           attachment=prof['att1'],
                           keyboard=search_in_keys.get_keyboard())
    else:
        await event.answer(message="Никого не нашли для тебя\n"
                                   "Не расстраивайся, попробуй поменять настройки поиска")
        await show_menu(event)