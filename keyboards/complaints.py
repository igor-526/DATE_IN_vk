from vkwave.bots import Keyboard, ButtonColor


complaint_keys = Keyboard()
complaint_keys.add_text_button(text='Отмена', payload={'command': 'cancel'},
                               color=ButtonColor.NEGATIVE)
complaint_keys.add_row()
complaint_keys.add_text_button(text='Фейковый профиль/данные', payload={'command': 'fake'},
                               color=ButtonColor.SECONDARY)
complaint_keys.add_row()
complaint_keys.add_text_button(text='Откровенный контент', payload={'command': 'sex_content'},
                               color=ButtonColor.SECONDARY)
complaint_keys.add_row()
complaint_keys.add_text_button(text='Коммерческая деятельность', payload={'command': 'commercial'},
                               color=ButtonColor.SECONDARY)
complaint_keys.add_row()
complaint_keys.add_text_button(text='Мошенничество', payload={'command': 'faking'},
                               color=ButtonColor.SECONDARY)
complaint_keys.add_row()
complaint_keys.add_text_button(text='Призывы к незаконным действиям', payload={'command': 'illegal'},
                               color=ButtonColor.SECONDARY)
complaint_keys.add_row()
complaint_keys.add_text_button(text='Неадекватное поведение/оскорбление', payload={'command': 'abuse'},
                               color=ButtonColor.SECONDARY)
complaint_keys.add_row()
complaint_keys.add_text_button(text='Младше 14 лет', payload={'command': 'age'},
                               color=ButtonColor.SECONDARY)
complaint_keys.add_row()
complaint_keys.add_text_button(text='Другое', payload={'command': 'other'},
                               color=ButtonColor.SECONDARY)
