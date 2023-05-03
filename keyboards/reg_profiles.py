from vkwave.bots import Keyboard, ButtonColor

reg_profile_keys = Keyboard()
reg_profile_keys.add_text_button(text="Регистрируюсь первый раз", payload={"command": "none"}, color=ButtonColor.PRIMARY)
reg_profile_keys.add_row()
reg_profile_keys.add_text_button(text="Вход через Telegram", payload={"command": "tg"}, color=ButtonColor.POSITIVE)
