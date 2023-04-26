from vkwave.bots import Keyboard, ButtonColor

prof_set_keys = Keyboard()
prof_set_keys.add_text_button(text="Назад", payload={"command": "menu"}, color=ButtonColor.PRIMARY)
prof_set_keys.add_row()
prof_set_keys.add_text_button(text="Имя", payload={"command": "menu"}, color=ButtonColor.SECONDARY)
prof_set_keys.add_text_button(text="Возраст", payload={"command": "menu"}, color=ButtonColor.SECONDARY)
prof_set_keys.add_row()
prof_set_keys.add_text_button(text="Пол", payload={"command": "menu"}, color=ButtonColor.SECONDARY)
prof_set_keys.add_text_button(text="Цели", payload={"command": "menu"}, color=ButtonColor.SECONDARY)
prof_set_keys.add_row()
prof_set_keys.add_text_button(text="Город", payload={"command": "menu"}, color=ButtonColor.SECONDARY)
prof_set_keys.add_text_button(text="Описание", payload={"command": "menu"}, color=ButtonColor.SECONDARY)
prof_set_keys.add_row()
prof_set_keys.add_text_button(text="Удал. фото", payload={"command": "menu"}, color=ButtonColor.SECONDARY)
prof_set_keys.add_text_button(text="Доб. фото", payload={"command": "menu"}, color=ButtonColor.SECONDARY)
prof_set_keys.add_row()
prof_set_keys.add_text_button(text="Изменить возраст поиска", payload={"command": "menu"}, color=ButtonColor.SECONDARY)
prof_set_keys.add_row()
prof_set_keys.add_text_button(text="Изменить пол поиска", payload={"command": "menu"}, color=ButtonColor.SECONDARY)
prof_set_keys.add_row()
prof_set_keys.add_text_button(text="Удалить профиль", payload={"command": "delete_profile"}, color=ButtonColor.NEGATIVE)