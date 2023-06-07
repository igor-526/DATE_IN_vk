from vkwave.bots import Keyboard, ButtonColor

menu_keys = Keyboard()
menu_keys.add_text_button(text="Поиск", payload={"command": "start"}, color=ButtonColor.POSITIVE)
menu_keys.add_text_button(text="Пары (0)", payload={"command": "matches"}, color=ButtonColor.POSITIVE)
menu_keys.add_row()
menu_keys.add_text_button(text="Обновить гео", payload={"command": "upd_geo"}, color=ButtonColor.PRIMARY)
menu_keys.add_text_button(text="Профиль", payload={"command": "profile"}, color=ButtonColor.SECONDARY)
