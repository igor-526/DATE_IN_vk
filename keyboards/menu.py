from vkwave.bots import Keyboard, ButtonColor
from dbase import count_matches


async def menu_keys(pr_id):
    match_count = await count_matches(pr_id)
    keys = Keyboard()
    keys.add_text_button(text="Поиск", payload={"command": "start"}, color=ButtonColor.POSITIVE)
    keys.add_text_button(text=f"Пары ({match_count})", payload={"command": "matches"}, color=ButtonColor.PRIMARY)
    keys.add_row()
    keys.add_text_button(text="Обновить гео", payload={"command": "upd_geo"}, color=ButtonColor.SECONDARY)
    keys.add_text_button(text="Профиль", payload={"command": "profile"}, color=ButtonColor.SECONDARY)
    return keys
