from vkwave.bots import Keyboard, ButtonColor

return_keys = Keyboard()
return_keys.add_text_button(text="Восстановить профиль", payload={"command": "return"}, color=ButtonColor.POSITIVE)