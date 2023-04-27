from vkwave.bots import Keyboard, ButtonColor

skip_keys = Keyboard()
skip_keys.add_text_button(text="Пропустить", payload={"command": "skip"}, color=ButtonColor.NEGATIVE)
skip_keys.add_row()
skip_keys.add_text_button(text="Назад", payload={"command": "back"}, color=ButtonColor.SECONDARY)