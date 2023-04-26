from vkwave.bots import Keyboard, ButtonColor

reg_keys = Keyboard()
reg_keys.add_text_button(text="Регистрация", payload={"command": "registration"}, color=ButtonColor.POSITIVE)