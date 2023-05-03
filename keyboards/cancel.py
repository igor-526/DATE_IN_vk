from vkwave.bots import Keyboard, ButtonColor

cancel_keys = Keyboard()
cancel_keys.add_text_button(text="Отмена", payload={"command": "cancel"}, color=ButtonColor.NEGATIVE)