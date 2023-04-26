from vkwave.bots import Keyboard, ButtonColor

menu_keys = Keyboard()
menu_keys.add_text_button(text="Начать поиск", payload={"command": "start"}, color=ButtonColor.POSITIVE)
menu_keys.add_row()
menu_keys.add_text_button(text="Мой профиль", payload={"command": "profile"}, color=ButtonColor.SECONDARY)
menu_keys.add_row()
menu_keys.add_text_button(text="Жалоба/баг", payload={"command": "complaint"}, color=ButtonColor.PRIMARY)