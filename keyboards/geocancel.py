from vkwave.bots import Keyboard, ButtonColor

geocancel_keys = Keyboard()
geocancel_keys.add_location_button()
geocancel_keys.add_row()
geocancel_keys.add_text_button(text="Отмена", payload={"command": "cancel"}, color=ButtonColor.NEGATIVE)
