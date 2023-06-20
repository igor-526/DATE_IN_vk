from vkwave.bots import Keyboard, ButtonColor

prof_set_keys = Keyboard()
prof_set_keys.add_text_button(text="Назад", payload={"command": "menu"}, color=ButtonColor.PRIMARY)
prof_set_keys.add_row()
prof_set_keys.add_text_button(text="Имя", payload={"command": "name"}, color=ButtonColor.SECONDARY)
prof_set_keys.add_text_button(text="Дата рождения", payload={"command": "bdate"}, color=ButtonColor.SECONDARY)
prof_set_keys.add_row()
prof_set_keys.add_text_button(text="Пол", payload={"command": "sex"}, color=ButtonColor.SECONDARY)
prof_set_keys.add_text_button(text="Цели", payload={"command": "purposes"}, color=ButtonColor.SECONDARY)
prof_set_keys.add_row()
prof_set_keys.add_text_button(text="Геопозиция", payload={"command": "geo"}, color=ButtonColor.SECONDARY)
prof_set_keys.add_text_button(text="Описание", payload={"command": "description"}, color=ButtonColor.SECONDARY)
prof_set_keys.add_row()
prof_set_keys.add_text_button(text="Удал. фото", payload={"command": "del_photos"}, color=ButtonColor.SECONDARY)
prof_set_keys.add_text_button(text="Доб. фото", payload={"command": "add_photos"}, color=ButtonColor.SECONDARY)
prof_set_keys.add_row()
prof_set_keys.add_text_button(text="Дополнительно", payload={"command": "desc_more"}, color=ButtonColor.PRIMARY)
prof_set_keys.add_text_button(text="Фильтры", payload={"command": "filters"}, color=ButtonColor.PRIMARY)
prof_set_keys.add_row()
prof_set_keys.add_text_button(text="Удалить профиль", payload={"command": "delete"}, color=ButtonColor.NEGATIVE)


filter_keys = Keyboard()
filter_keys.add_text_button(text="Назад", payload={"command": "back"}, color=ButtonColor.PRIMARY)
filter_keys.add_text_button(text="Возраст", payload={"command": "age_f"}, color=ButtonColor.SECONDARY)
filter_keys.add_row()
filter_keys.add_text_button(text="Пол", payload={"command": "sex_f"}, color=ButtonColor.SECONDARY)
filter_keys.add_text_button(text="Расстояние", payload={"command": "km_f"}, color=ButtonColor.SECONDARY)


profile_inline_keys = Keyboard(inline=True)
profile_inline_keys.add_callback_button(text='Рост', payload={'command': 'height'})
profile_inline_keys.add_callback_button(text='Хобби', payload={'command': 'hobby'})
profile_inline_keys.add_row()
profile_inline_keys.add_callback_button(text='Занятость', payload={'command': 'busy'})
profile_inline_keys.add_callback_button(text='Дети', payload={'command': 'children'})
profile_inline_keys.add_row()
profile_inline_keys.add_callback_button(text='Животные', payload={'command': 'animals'})
profile_inline_keys.add_callback_button(text='Вр. привычки', payload={'command': 'habits'})
profile_inline_keys.add_row()
profile_inline_keys.add_callback_button(text='В профиль', payload={'command': 'profile'})


backin_keys = Keyboard(inline=True)
backin_keys.add_callback_button(text='Назад', payload={'command': 'back'})
backin_keys.add_callback_button(text='Очистить', payload={'command': 'clean'})


children_keys = Keyboard(inline=True)
children_keys.add_callback_button(text='Имею ребёнка/детей', payload={'command': 'yes'})
children_keys.add_row()
children_keys.add_callback_button(text='Планирую', payload={'command': 'plan'})
children_keys.add_row()
children_keys.add_callback_button(text='Пока не планирую', payload={'command': 'no'})
children_keys.add_row()
children_keys.add_callback_button(text='Назад', payload={'command': 'back'})
children_keys.add_callback_button(text='Очистить', payload={'command': 'clean'})


busy_keys = Keyboard(inline=True)
busy_keys.add_callback_button(text='не учусь/не работаю', payload={'command': 'none'})
busy_keys.add_callback_button(text='учусь/не работаю', payload={'command': 'learning'})
busy_keys.add_row()
busy_keys.add_callback_button(text='не учусь/работаю', payload={'command': 'working'})
busy_keys.add_callback_button(text='учусь/работаю', payload={'command': 'and'})
busy_keys.add_row()
busy_keys.add_callback_button(text='Назад', payload={'command': 'back'})
busy_keys.add_callback_button(text='Очистить', payload={'command': 'clean'})


proftg_keys = Keyboard(inline=True)
proftg_keys.add_callback_button(text='фото', payload={'command': 'get_photo'})
proftg_keys.add_callback_button(text='Описание', payload={'command': 'get_description'})
