from vkwave.bots import Keyboard, ButtonColor

code_keys = Keyboard()
code_keys.add_text_button(text="Отправить ещё раз", payload={"command": "repeat"}, color=ButtonColor.SECONDARY)
code_keys.add_text_button(text="Отмена", payload={"command": "cancel"}, color=ButtonColor.NEGATIVE)