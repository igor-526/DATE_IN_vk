from vkwave.bots import Keyboard, ButtonColor

sex_keys = Keyboard()
sex_keys.add_text_button(text="Мужчина &#128104;", payload={"command": "male"}, color=ButtonColor.PRIMARY)
sex_keys.add_text_button(text="Девушка &#128105;", payload={"command": "female"}, color=ButtonColor.NEGATIVE)
sex_keys.add_row()
sex_keys.add_text_button(text="Назад", payload={"command": "back"}, color=ButtonColor.SECONDARY)