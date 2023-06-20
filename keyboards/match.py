from vkwave.bots import Keyboard, ButtonColor

newmatch_keys = Keyboard()
newmatch_keys.add_text_button(text="Меню", payload={"command": "menu"}, color=ButtonColor.SECONDARY)
newmatch_keys.add_text_button(text="\U000025B6", payload={"command": "next"}, color=ButtonColor.SECONDARY)
newmatch_keys.add_row()
newmatch_keys.add_text_button(text="Просмотренные", payload={"command": "showed"}, color=ButtonColor.PRIMARY)


nomatch_keys = Keyboard()
nomatch_keys.add_text_button(text="Начать поиск", payload={"command": "search"}, color=ButtonColor.POSITIVE)
nomatch_keys.add_row()
nomatch_keys.add_text_button(text="Меню", payload={"command": "menu"}, color=ButtonColor.SECONDARY)
nomatch_keys.add_text_button(text="Просмотренные", payload={"command": "showed"}, color=ButtonColor.PRIMARY)


oldmatch_keys = Keyboard()
oldmatch_keys.add_text_button(text="\U000025C0", payload={"command": "prev"}, color=ButtonColor.SECONDARY)
oldmatch_keys.add_text_button(text="\U000025B6", payload={"command": "next"}, color=ButtonColor.SECONDARY)
oldmatch_keys.add_row()
oldmatch_keys.add_text_button(text="Меню", payload={"command": "menu"}, color=ButtonColor.SECONDARY)


oldnomatch_keys = Keyboard()
oldnomatch_keys.add_text_button(text="Начать поиск", payload={"command": "search"}, color=ButtonColor.SECONDARY)
oldnomatch_keys.add_text_button(text="Меню", payload={"command": "menu"}, color=ButtonColor.SECONDARY)


async def match_in_keys(contacts):
    matchin_keys = Keyboard(inline=True)
    matchin_keys.add_callback_button(text='фото', payload={'command': 'get_photo'})
    matchin_keys.add_callback_button(text='Описание', payload={'command': 'get_description'})
    matchin_keys.add_row()
    matchin_keys.add_callback_button(text='Пожаловаться', payload={'command': 'complaint'})
    matchin_keys.add_row()
    if contacts['cont_vk']:
        matchin_keys.add_link_button(text='ВК', link=contacts['cont_vk'])
    if contacts['cont_tg']:
        matchin_keys.add_link_button(text='TG', link=contacts['cont_tg'])
    return matchin_keys
