from vkwave.bots import Keyboard, ButtonColor

back_keys = Keyboard()
back_keys.add_text_button(text="Назад", payload={"command": "back"}, color=ButtonColor.SECONDARY)