from vkwave.bots import Keyboard, ButtonColor

menu_keys = Keyboard()
menu_keys.add_text_button(text="Начать поиск", payload={"command": "start"}, color=ButtonColor.POSITIVE)
menu_keys.add_text_button(text="Пары (0)", payload={"command": "matches"}, color=ButtonColor.POSITIVE)
menu_keys.add_row()
menu_keys.add_text_button(text="Обновить геолокацию", payload={"command": "upd_geo"}, color=ButtonColor.PRIMARY)
menu_keys.add_text_button(text="Мой профиль", payload={"command": "profile"}, color=ButtonColor.SECONDARY)