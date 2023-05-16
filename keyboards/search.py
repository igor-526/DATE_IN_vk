from vkwave.bots import Keyboard, ButtonColor

search_keys = Keyboard()
search_keys.add_text_button(text="ЛАЙК", payload={"command": "like"}, color=ButtonColor.NEGATIVE)
search_keys.add_text_button(text="Далее", payload={"command": "pass"}, color=ButtonColor.POSITIVE)
search_keys.add_row()
search_keys.add_text_button(text="Пожаловаться", payload={"command": "complaint"}, color=ButtonColor.SECONDARY)
search_keys.add_row()
search_keys.add_text_button(text="Меню", payload={"command": "menu"}, color=ButtonColor.SECONDARY)
