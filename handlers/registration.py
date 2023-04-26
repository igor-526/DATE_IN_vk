from vkwave.bots.fsm import StateFilter, ANY_STATE, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.types.objects import MessagesMessageAttachmentType
from vkwave.bots import (SimpleBotEvent,
                         DefaultRouter,
                         simple_bot_message_handler,
                         Keyboard)
from FSM import (fsm,
                 RegistrationFSM,
                 MenuFSM)
from keyboards import (reg_profile_keys,
                       yesno_keys,
                       sexf_keys,
                       sex_keys,
                       skip_keys,
                       menu_keys)
from vkapi import (vkuser_info,
                   find_city)
from validators import (valid_name,
                        valid_age,
                        valid_purpose,
                        valid_description)
from funcs import (gen_purposes,
                   gen_profile)
from dbase import (reg_profile)

registration_router = DefaultRouter()


async def ask_sex(sex, event):
    if sex == 2:
        await event.answer(message="А вы мужчина?",
                           keyboard=yesno_keys.get_keyboard())
        await fsm.set_state(state=RegistrationFSM.reg_sex_auto, event=event, for_what=ForWhat.FOR_USER)
    if sex == 1:
        await event.answer(message="А вы девушка?",
                           keyboard=yesno_keys.get_keyboard())
        await fsm.set_state(state=RegistrationFSM.reg_sex_auto, event=event, for_what=ForWhat.FOR_USER)
    if not sex:
        await event.answer(message="А кто вы?",
                           keyboard=sex_keys.get_keyboard())
        await fsm.set_state(state=RegistrationFSM.reg_sex, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(registration_router, filters.CommandsFilter('reset'),
                            StateFilter(fsm=fsm, state=ANY_STATE, for_what=ForWhat.FOR_USER))
async def reset(event: SimpleBotEvent):
    await fsm.finish(event=event, for_what=ForWhat.FOR_USER)
    return 'succ'


@simple_bot_message_handler(registration_router, filters.PayloadFilter({"command": "registration"}),
                            StateFilter(fsm=fsm, state=RegistrationFSM.registration, for_what=ForWhat.FOR_USER))
async def ask_profile(event: SimpleBotEvent):
    await event.answer(message="Подскажите, у Вас уже есть профиль на сайте или в TG?",
                       keyboard=reg_profile_keys.get_keyboard())
    await fsm.set_state(event=event, state=RegistrationFSM.reg_profile, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(registration_router,
                            StateFilter(fsm=fsm, state=RegistrationFSM.registration, for_what=ForWhat.FOR_USER))
async def ask_profile_invalid(event: SimpleBotEvent):
    return "Я вас не понимаю &#128532;\n" \
           "Пожалуйста, выберите действие на клавиатуре"


@simple_bot_message_handler(registration_router, filters.PayloadFilter({"command": "tg"}),
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_profile, for_what=ForWhat.FOR_USER))
async def reg_profile_tg(event: SimpleBotEvent):
    return "К сожалению, функция ещё не реализована (tg)&#128532;"


@simple_bot_message_handler(registration_router, filters.PayloadFilter({"command": "site"}),
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_profile, for_what=ForWhat.FOR_USER))
async def reg_profile_site(event: SimpleBotEvent):
    return "К сожалению, функция ещё не реализована (site)&#128532;"


@simple_bot_message_handler(registration_router, filters.PayloadFilter({"command": "none"}),
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_profile, for_what=ForWhat.FOR_USER))
async def reg_profile_none(event: SimpleBotEvent):
    await fsm.set_state(event=event, state=RegistrationFSM.reg_name_auto, for_what=ForWhat.FOR_USER)
    profile_info = await vkuser_info(event.user_id)
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'info': profile_info})
    await event.answer(message=f"Тогда начнём &#128521;\n"
                               f"Тебя зовут {profile_info['name']}?",
                       keyboard=yesno_keys.get_keyboard())


@simple_bot_message_handler(registration_router,
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_profile, for_what=ForWhat.FOR_USER))
async def reg_profile_invalid(event: SimpleBotEvent):
    return "Я вас не понимаю &#128532;\n" \
           "Пожалуйста, выберите действие на клавиатуре"


@simple_bot_message_handler(registration_router, filters.PayloadFilter({"command": "yes"}),
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_name_auto, for_what=ForWhat.FOR_USER))
async def reg_name_auto_yes(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    age = data['info']['age']
    name = data['info']['name']
    await event.answer("Записал &#128521;\n"
                       "Теперь нужно определиться с возрастом")
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'name': name})
    if age:
        await event.answer(message=f"Тебе {age}?",
                           keyboard=yesno_keys.get_keyboard())
        await fsm.set_state(state=RegistrationFSM.reg_age_auto, event=event, for_what=ForWhat.FOR_USER)
    else:
        await event.answer(message="Сколько тебе лет?",
                           keyboard=Keyboard.get_empty_keyboard())
        await fsm.set_state(state=RegistrationFSM.reg_age, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(registration_router, filters.PayloadFilter({"command": "no"}),
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_name_auto, for_what=ForWhat.FOR_USER))
async def reg_name_auto_no(event: SimpleBotEvent):
    await event.answer(message='Как же тогда тебя зовут? &#128527;',
                       keyboard=Keyboard.get_empty_keyboard())
    await fsm.set_state(state=RegistrationFSM.reg_name, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(registration_router,
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_name_auto, for_what=ForWhat.FOR_USER))
async def reg_name_auto_invalid(event: SimpleBotEvent):
    return "Я вас не понимаю &#128532;\n" \
           "Пожалуйста, выберите действие на клавиатуре"


@simple_bot_message_handler(registration_router,
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_name, for_what=ForWhat.FOR_USER))
async def reg_name(event: SimpleBotEvent):
    validator = await valid_name(event.text)
    if validator == 'valid':
        data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
        age = data['info']['age']
        await event.answer("Записал &#128521;\n"
                           "Теперь нужно определиться с возрастом")
        await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'name': event.text})
        if age:
            await event.answer(message=f"Тебе {age}?",
                               keyboard=yesno_keys.get_keyboard())
            await fsm.set_state(state=RegistrationFSM.reg_age_auto, event=event, for_what=ForWhat.FOR_USER)
        else:
            await event.answer(message="Сколько тебе лет?",
                               keyboard=Keyboard.get_empty_keyboard())
            await fsm.set_state(state=RegistrationFSM.reg_age, event=event, for_what=ForWhat.FOR_USER)
    elif validator == 'invalid':
        return 'Я не верю в такое имя &#128563;\n' \
               'Попробуй ввести ещё раз'
    elif validator == 'obscene':
        return 'И кто же тебя так назвал.. &#128560;\n' \
               'Давай попробуем ещё раз, только нормально &#128514;'


@simple_bot_message_handler(registration_router, filters.PayloadFilter({"command": "yes"}),
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_age_auto, for_what=ForWhat.FOR_USER))
async def reg_age_auto_yes(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    age = data['info']['age']
    await event.answer(message="Записал &#128521;\n"
                               "А кого будем искать?",
                       keyboard=sexf_keys.get_keyboard())
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'age': age})
    await fsm.set_state(state=RegistrationFSM.reg_sex_f, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(registration_router, filters.PayloadFilter({"command": "no"}),
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_age_auto, for_what=ForWhat.FOR_USER))
async def reg_age_auto_no(event: SimpleBotEvent):
    await event.answer(message='А сколько же тебе тогда? &#128527;\n'
                               'Учти, что врать нехорошо!',
                       keyboard=Keyboard.get_empty_keyboard())
    await fsm.set_state(state=RegistrationFSM.reg_age, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(registration_router,
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_age_auto, for_what=ForWhat.FOR_USER))
async def reg_age_auto_invalid(event: SimpleBotEvent):
    return "Я вас не понимаю &#128532;\n" \
           "Пожалуйста, выберите действие на клавиатуре"


@simple_bot_message_handler(registration_router,
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_age, for_what=ForWhat.FOR_USER))
async def reg_age(event: SimpleBotEvent):
    validator = await valid_age(event.text, None)
    if validator == "valid":
        await event.answer(message="Записал &#128521;\n"
                                   "А кого будем искать?",
                           keyboard=sexf_keys.get_keyboard())
        await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'age': event.text})
        await fsm.set_state(state=RegistrationFSM.reg_sex_f, event=event, for_what=ForWhat.FOR_USER)
    elif validator == "invalid":
        return "Пожалуйста, напиши свой возраст\n" \
               "Просто циферку"
    elif validator == "too_old":
        return "Да ладно\n" \
               "Я не верю. Попробуй ещё раз"


@simple_bot_message_handler(registration_router, filters.PayloadFilter({"command": "male"}),
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_sex_f, for_what=ForWhat.FOR_USER))
async def reg_sexf_man(event: SimpleBotEvent):
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'sexf': 2})
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    sex = data['info']['sex']
    await ask_sex(sex, event)


@simple_bot_message_handler(registration_router, filters.PayloadFilter({"command": "female"}),
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_sex_f, for_what=ForWhat.FOR_USER))
async def reg_sexf_woman(event: SimpleBotEvent):
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'sexf': 1})
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    sex = data['info']['sex']
    await ask_sex(sex, event)


@simple_bot_message_handler(registration_router, filters.PayloadFilter({"command": "all"}),
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_sex_f, for_what=ForWhat.FOR_USER))
async def reg_sexf_all(event: SimpleBotEvent):
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'sexf': 3})
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    sex = data['info']['sex']
    await ask_sex(sex, event)


@simple_bot_message_handler(registration_router,
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_sex_f, for_what=ForWhat.FOR_USER))
async def reg_age_auto_invalid(event: SimpleBotEvent):
    return "Я вас не понимаю &#128532;\n" \
           "Пожалуйста, выберите действие на клавиатуре"


@simple_bot_message_handler(registration_router, filters.PayloadFilter({"command": "yes"}),
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_sex_auto, for_what=ForWhat.FOR_USER))
async def reg_sex_auto_yes(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    sex = data['info']['sex']
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'sex': sex})
    await fsm.set_state(state=RegistrationFSM.reg_age_min, event=event, for_what=ForWhat.FOR_USER)
    await event.answer(message="От какого возраста будем искать?",
                       keyboard=Keyboard.get_empty_keyboard())


@simple_bot_message_handler(registration_router, filters.PayloadFilter({"command": "no"}),
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_sex_auto, for_what=ForWhat.FOR_USER))
async def reg_sex_auto_no(event: SimpleBotEvent):
    await event.answer(message="А кто же тогда?",
                       keyboard=sex_keys.get_keyboard())
    await fsm.set_state(state=RegistrationFSM.reg_sex, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(registration_router,
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_sex_auto, for_what=ForWhat.FOR_USER))
async def reg_sex_auto_invalid(event: SimpleBotEvent):
    return "Я вас не понимаю &#128532;\n" \
           "Пожалуйста, выберите действие на клавиатуре"


@simple_bot_message_handler(registration_router, filters.PayloadFilter({"command": "male"}),
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_sex, for_what=ForWhat.FOR_USER))
async def reg_sex_male(event: SimpleBotEvent):
    await event.answer(message="Допустим\n"
                               "От какого возраста будем искать?",
                       keyboard=Keyboard.get_empty_keyboard())
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'sex': 2})
    await fsm.set_state(state=RegistrationFSM.reg_age_min, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(registration_router, filters.PayloadFilter({"command": "female"}),
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_sex, for_what=ForWhat.FOR_USER))
async def reg_sex_female(event: SimpleBotEvent):
    await event.answer(message="Допустим\n"
                               "От какого возраста будем искать?",
                       keyboard=Keyboard.get_empty_keyboard())
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'sex': 1})
    await fsm.set_state(state=RegistrationFSM.reg_age_min, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(registration_router,
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_sex, for_what=ForWhat.FOR_USER))
async def reg_sex_invalid(event: SimpleBotEvent):
    return "Я вас не понимаю &#128532;\n" \
           "Пожалуйста, выберите действие на клавиатуре"


@simple_bot_message_handler(registration_router,
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_age_min, for_what=ForWhat.FOR_USER))
async def reg_age_min(event: SimpleBotEvent):
    validator = await valid_age(event.text, None)
    if validator == "valid":
        await event.answer(message="С этим определились &#128521;\n"
                                   "А максимальный возраст будет какой?")
        await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'age_min': event.text})
        await fsm.set_state(state=RegistrationFSM.reg_age_max, event=event, for_what=ForWhat.FOR_USER)
    elif validator == "invalid":
        return "Пожалуйста, напиши минимальный возраст для поиска\n" \
               "Просто циферку"
    elif validator == "too_old":
        return "Тут уже проще будет поискать на кладбище\n" \
               "Давай попробуем кого нибудь помладше"


@simple_bot_message_handler(registration_router,
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_age_max, for_what=ForWhat.FOR_USER))
async def reg_age_max(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    age_min = data['age_min']
    city = data['info']['city_title']
    validator = await valid_age(event.text, age_min)
    if validator == "valid":
        await event.answer(message="И с этим определились &#128521;\n"
                                   "Теперь зададим географические настройки")
        await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'age_max': event.text})
        if city:
            await event.answer(message=f'Ваш город {city}?',
                               keyboard=yesno_keys.get_keyboard())
            await fsm.set_state(state=RegistrationFSM.reg_city_auto, event=event, for_what=ForWhat.FOR_USER)
        else:
            await event.answer("Из какого вы города?")
            await fsm.set_state(state=RegistrationFSM.reg_city, event=event, for_what=ForWhat.FOR_USER)
    elif validator == "invalid":
        return "Пожалуйста, напиши максимальный возраст для поиска\n" \
               "Просто циферку"
    elif validator == "too_old":
        return "Тут уже проще будет поискать на кладбище\n" \
               "Давай попробуем кого нибудь помладше"
    elif validator == "more_min":
        return "Максимальный возраст не может быть меньше минимального\n" \
               "Попробуй ещё раз!"


@simple_bot_message_handler(registration_router, filters.PayloadFilter({"command": "yes"}),
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_city_auto, for_what=ForWhat.FOR_USER))
async def reg_city_auto_yes(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    purposes = await gen_purposes()
    city_title = data['info']['city_title']
    city_id = data['info']['city_id']
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'city_title': city_title, 'city_id': city_id,
                                                                           'purposes_len': purposes['len']})
    msg = 'Почти последний шаг - определиться с целями!\nПожалуйста, через запятую перечислите номера целей\n\n'
    msg += purposes['msg']
    await event.answer(message=msg,
                       keyboard=Keyboard.get_empty_keyboard())
    await fsm.set_state(state=RegistrationFSM.reg_purpose, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(registration_router, filters.PayloadFilter({"command": "no"}),
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_city_auto, for_what=ForWhat.FOR_USER))
async def reg_city_auto_no(event: SimpleBotEvent):
    await event.answer(message="Не угадал\n"
                               "Из какого ты города?")
    await fsm.set_state(state=RegistrationFSM.reg_city, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(registration_router,
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_city_auto, for_what=ForWhat.FOR_USER))
async def reg_city_auto_invalid(event: SimpleBotEvent):
    return "Я вас не понимаю &#128532;\n" \
           "Пожалуйста, выберите действие на клавиатуре"


@simple_bot_message_handler(registration_router,
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_city, for_what=ForWhat.FOR_USER))
async def reg_city(event: SimpleBotEvent):
    result = await find_city(event.text)
    if result['city_id']:
        await event.answer(f'Установлен город {result["city_title"]}')
        purposes = await gen_purposes()
        await fsm.add_data(event=event, for_what=ForWhat.FOR_USER,
                           state_data={'city_title': result["city_title"], 'city_id': result["city_id"],
                                       'purposes_len': purposes['len']})
        msg = 'Почти последний шаг - определиться с целями!\nПожалуйста, через запятую или пробел ' \
              'перечислите номера целей\n\n'
        msg += purposes['msg']
        await event.answer(message=msg,
                           keyboard=Keyboard.get_empty_keyboard())
        await fsm.set_state(state=RegistrationFSM.reg_purpose, event=event, for_what=ForWhat.FOR_USER)
    else:
        return "Не удалось найти такой город\n" \
               "Попробуйте ввести название полностью и без опечаток"


@simple_bot_message_handler(registration_router,
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_purpose, for_what=ForWhat.FOR_USER))
async def reg_purpose(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    purpose_len = data['purposes_len']
    validator = await valid_purpose(event.text, purpose_len)
    if validator == 'invalid':
        return 'Я так не понял\n' \
               'Пожалуйста, введите только номера целей, отделяя их запятой или пробелом'
    else:
        await event.answer(message='Супер! Отправь мне фотографии (до 3 шт., потом можно будет добавить), которые'
                                   'будешь гордо демонстрировать другим пользователям сервиса\n'
                                   'Если хочется пользоваться без фотографий (что мы очень не рекомендуем) или '
                                   'отправить их потом, нажми кнопку "Пропустить"',
                           keyboard=skip_keys.get_keyboard())
        await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={"purposes": validator})
        await fsm.set_state(state=RegistrationFSM.reg_photo, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(registration_router,
                            filters.AttachmentTypeFilter(attachment_type=MessagesMessageAttachmentType.PHOTO),
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_photo, for_what=ForWhat.FOR_USER))
async def reg_photo(event: SimpleBotEvent):
    atts = event.attachments
    photos = []
    for photo in atts:
        photos.append(photo.photo.sizes[-1].url)
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'photos': photos})
    await event.answer(message="Готово! И последний шаг - напиши мне какой-нибудь текст, который заинтересует любого "
                               "и заставит нажать кнопку лайка!\n"
                               "Если хочется придумать позже, или вообще не добавлять (что мы так же не рекомендуем!),"
                               " просто нажми кнопку 'Пропустить'",
                       keyboard=skip_keys.get_keyboard())
    await fsm.set_state(state=RegistrationFSM.reg_description, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(registration_router, filters.PayloadFilter({"command": "skip"}),
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_photo, for_what=ForWhat.FOR_USER))
async def reg_photo_skip(event: SimpleBotEvent):
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'photos': []})
    await event.answer(message="Готово! И последний шаг - напиши мне какой-нибудь текст, который заинтересует любого "
                               "и заставит нажать кнопку лайка!\n"
                               "Если хочется придумать позже, или вообще не добавлять (что мы так же не рекомендуем!),"
                               " просто нажми кнопку 'Пропустить'",
                       keyboard=skip_keys.get_keyboard())
    await fsm.set_state(event=event, for_what=ForWhat.FOR_USER, state=RegistrationFSM.reg_description)


@simple_bot_message_handler(registration_router,
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_photo, for_what=ForWhat.FOR_USER))
async def reg_photo_invalid(event: SimpleBotEvent):
    return "Просто отправь мне фотографии или нажми кнопку 'Пропустить'"


@simple_bot_message_handler(registration_router, filters.PayloadFilter({"command": "skip"}),
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_description, for_what=ForWhat.FOR_USER))
async def reg_description_skip(event: SimpleBotEvent):
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'description': None})
    await event.answer(message='Наконец-то регистрация завершена!\n'
                               'Этот профиль можно будет использовать для сайта и нашего бота в Telegram!\n'
                               'Вот так он выглядит:')
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    await reg_profile(event.user_id, data)
    data = await gen_profile(event.user_id)
    await event.answer(message=data['msg1'],
                       attachment=data['att1'])
    if data['msg2'] or data['att2']:
        await event.answer(message=data['msg2'],
                           attachment=data['att2'])
    await event.answer(message='Выберите действие:',
                       keyboard=menu_keys.get_keyboard())
    await fsm.set_state(state=MenuFSM.menu, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(registration_router,
                            StateFilter(fsm=fsm, state=RegistrationFSM.reg_description, for_what=ForWhat.FOR_USER))
async def reg_description(event: SimpleBotEvent):
    validator = await valid_description(event.text)
    if validator == 'valid':
        await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'description': event.text})
        await event.answer(message='Наконец-то регистрация завершена!\n'
                                   'Этот профиль можно будет использовать для сайта и нашего бота в Telegram!\n'
                                   'Вот так он выглядит:')
        data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
        await reg_profile(event.user_id, data)
        data = await gen_profile(event.user_id)
        await event.answer(message=data['msg1'],
                           attachment=data['att1'])
        if data['msg2'] or data['att2']:
            await event.answer(message=data['msg2'],
                               attachment=data['att2'])
        await event.answer(message='Выберите действие:',
                           keyboard=menu_keys.get_keyboard())
        await fsm.set_state(state=MenuFSM.menu, event=event, for_what=ForWhat.FOR_USER)
    elif validator == 'invalid':
        return "Мы против нецензурной лексики\n" \
               "Попробуй переписать так, чтобы её там не было"
