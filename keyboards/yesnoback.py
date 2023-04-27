from vkwave.bots import Keyboard, ButtonColor

yesnoback_keys = Keyboard()
yesnoback_keys.add_text_button(text="Да", payload={"command": "yes"}, color=ButtonColor.POSITIVE)
yesnoback_keys.add_text_button(text="Нет", payload={"command": "no"}, color=ButtonColor.NEGATIVE)
yesnoback_keys.add_row()
yesnoback_keys.add_text_button(text="Назад", payload={"command": "back"}, color=ButtonColor.SECONDARY)