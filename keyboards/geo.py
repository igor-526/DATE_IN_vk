from vkwave.bots import Keyboard, ButtonColor

geo_keys = Keyboard()
geo_keys.add_location_button()
geo_keys.add_row()
geo_keys.add_text_button(text="Назад", payload={"command": "back"}, color=ButtonColor.NEGATIVE)
