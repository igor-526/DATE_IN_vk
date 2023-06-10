from vkwave.bots import Keyboard, ButtonColor

search_keys = Keyboard()
search_keys.add_text_button(text="&#10060;", payload={"command": "pass"}, color=ButtonColor.SECONDARY)
search_keys.add_text_button(text="&#10084;", payload={"command": "like"}, color=ButtonColor.SECONDARY)
search_keys.add_row()
search_keys.add_text_button(text="Меню", payload={"command": "menu"}, color=ButtonColor.PRIMARY)

searchin_keys = Keyboard(inline=True)
searchin_keys.add_callback_button(text='фото', payload={'command': 'get_photo'})
searchin_keys.add_callback_button(text='Описание', payload={'command': 'get_description'})
searchin_keys.add_row()
searchin_keys.add_callback_button(text='Пожаловаться', payload={'command': 'complaint'})
