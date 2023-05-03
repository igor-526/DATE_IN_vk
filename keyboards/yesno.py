from vkwave.bots import Keyboard, ButtonColor

yesno_keys = Keyboard()
yesno_keys.add_text_button(text="Да", payload={"command": "yes"}, color=ButtonColor.POSITIVE)
yesno_keys.add_text_button(text="Нет", payload={"command": "no"}, color=ButtonColor.NEGATIVE)
