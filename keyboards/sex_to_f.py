from vkwave.bots import Keyboard, ButtonColor

sexf_keys = Keyboard()
sexf_keys.add_text_button(text="Мужчин &#128104;", payload={"command": "male"}, color=ButtonColor.PRIMARY)
sexf_keys.add_text_button(text="Девушек &#128105;", payload={"command": "female"}, color=ButtonColor.NEGATIVE)
sexf_keys.add_row()
sexf_keys.add_text_button(text="Всех! &#128104;&#128105;", payload={"command": "all"}, color=ButtonColor.POSITIVE)
sexf_keys.add_row()
sexf_keys.add_text_button(text="Назад", payload={"command": "back"}, color=ButtonColor.SECONDARY)