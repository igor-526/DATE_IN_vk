from FSM import (fsm,
                 Reg)
from vkwave.bots import SimpleBotEvent
from keyboards import (yesnoback_keys,
                       reg_profile_keys,
                       back_keys,
                       sex_keys,
                       geo_keys,
                       skip_keys,
                       sexf_keys,
                       )
from vkwave.bots.fsm import ForWhat
from funcs import gen_purposes, generate_profile_forview
from dbase import add_profile, add_settings, add_profile_photos
import datetime


async def invalid(event: SimpleBotEvent, keys):
    await event.answer(message="Я вас не понимаю &#128532;\n" \
                               "Пожалуйста, выберите действие на клавиатуре",
                       keyboard=keys)


async def start_registration(event: SimpleBotEvent):
    await event.answer(message="Подскажите, у Вас уже есть профиль на сайте или в TG?",
                       keyboard=reg_profile_keys.get_keyboard())
    await fsm.set_state(event=event, state=Reg.profile, for_what=ForWhat.FOR_USER)


async def f_ask_name_auto(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    profile_info = data['vk']
    await event.answer(message=f"Тогда начнём &#128521;\n"
                               f"Тебя зовут {profile_info['name']}?",
                       keyboard=yesnoback_keys.get_keyboard())
    await fsm.set_state(state=Reg.name_auto, event=event, for_what=ForWhat.FOR_USER)


async def f_ask_name_manual(event: SimpleBotEvent):
    await event.answer(message=f'Как же тогда тебя зовут? &#128527;\n'
                               f'Учти, что имя после регистрации можно будет поменять только 1 раз!',
                       keyboard=back_keys.get_keyboard())
    await fsm.set_state(state=Reg.name_manual, event=event, for_what=ForWhat.FOR_USER)


async def f_reg_bdate(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    if not data['vk']['bdate']:
        await event.answer("Записал &#128521;\n"
                           "Не вижу твою дату рождения\n"
                           "Напиши мне её, пожалуйста, в формате 'ДД.ММ.ГГГГ'\n"
                           "Учти, что после регистрации её можно будет поменять только один раз!",
                           keyboard=back_keys.get_keyboard())
        await fsm.set_state(state=Reg.bdate_manual, event=event, for_what=ForWhat.FOR_USER)
    elif len(data['vk']['bdate'].split('.')) == 2:
        await event.answer("Записал &#128521;\n"
                           "Вижу твой день рождения! Но мне нужен ещё и год\n"
                           "Напиши мне его, пожалуйста, в формате 'ГГГГ'\n"
                           "Учти, что после регистрации дату рождения можно будет поменять только один раз!",
                           keyboard=back_keys.get_keyboard())
        await fsm.set_state(state=Reg.bdate_year, event=event, for_what=ForWhat.FOR_USER)
    elif len(data['vk']['bdate'].split('.')) == 3:
        await event.answer(f"Записал &#128521;\n"
                           f"Вижу твою полную дату рождения - {data['vk']['bdate']}\n"
                           f"Это же она?",
                           keyboard=yesnoback_keys.get_keyboard())
        await fsm.set_state(state=Reg.bdate_auto, event=event, for_what=ForWhat.FOR_USER)


async def f_reg_bdate_manual(event: SimpleBotEvent):
    await event.answer(message="Тогда напиши мне её, пожалуйста, в формате 'ДД.ММ.ГГГГ'\n"
                               "Учти, что после регистрации её можно будет поменять только один раз!",
                       keyboard=back_keys.get_keyboard())
    await fsm.set_state(state=Reg.bdate_manual, event=event, for_what=ForWhat.FOR_USER)


async def f_reg_sex(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    sex = data['vk']['sex']
    if sex:
        await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'sex': data['vk']['sex']})
        await event.answer(message=f'Записал &#128521;\n'
                                   f'Надеюсь, твой пол - {"мужской" if sex==2 else "женский"}?\n'
                                   f'Если это не так, то потом можно будет поменять в настройках\n'
                                   f'Но только один раз!')
        await f_reg_geo(event)

    elif not sex:
        await event.answer(message='Не удалось определить твой пол\n'
                                   'Помоги, пожалуйста',
                           keyboard=sex_keys.get_keyboard())
        await fsm.set_state(state=Reg.sex_manual, event=event, for_what=ForWhat.FOR_USER)


async def f_reg_geo(event: SimpleBotEvent):
    await event.answer(message='Мне нужно знать твоё местоположение (можно примерное)\n'
                               'Это для того, чтобы подбирать тебе анкеты поближе',
                       keyboard=geo_keys.get_keyboard())
    await fsm.set_state(state=Reg.geo, event=event, for_what=ForWhat.FOR_USER)


async def f_reg_photo(event: SimpleBotEvent):
    await event.answer(message='Супер! Отправь мне фотографии (до 3 шт., потом можно будет добавить), которые'
                               'будешь гордо демонстрировать другим пользователям сервиса\n'
                               'Если хочется пользоваться без фотографий (что мы очень не рекомендуем) или '
                               'отправить их потом, нажми кнопку "Пропустить"',
                       keyboard=skip_keys.get_keyboard())
    await fsm.set_state(state=Reg.photo, event=event, for_what=ForWhat.FOR_USER)


async def f_reg_description(event: SimpleBotEvent):
    await event.answer(message="Готово! Почти шаг - напиши мне какой-нибудь текст, который заинтересует любого "
                               "и заставит нажать кнопку лайка!\n"
                               "Если хочется придумать позже, или вообще не добавлять (что мы так же не рекомендуем!),"
                               " просто нажми кнопку 'Пропустить'",
                       keyboard=skip_keys.get_keyboard())
    await fsm.set_state(state=Reg.description, event=event, for_what=ForWhat.FOR_USER)


async def f_reg_purposes(event: SimpleBotEvent):
    msg = 'Последний шаг - определиться с целями!\nПожалуйста, через запятую или пробел ' \
          'перечислите номера целей\n\n'
    msg += await gen_purposes()
    await event.answer(message=msg,
                       keyboard=back_keys.get_keyboard())
    await fsm.set_state(state=Reg.purposes, event=event, for_what=ForWhat.FOR_USER)

async def f_reg_sexf(event: SimpleBotEvent):
    await event.answer(message='С твоим профилем всё!\nОсталось определиться с настройками поиска\n'
                               'Тут гораздо меньше. Детальнее потом можно будет настроить в меню')
    await event.answer(message='Кого мы будем искать?',
                       keyboard=sexf_keys.get_keyboard())
    await fsm.set_state(state=Reg.f_sex, event=event, for_what=ForWhat.FOR_USER)


async def f_reg_age_min(event: SimpleBotEvent):
    await event.answer(message='С этим определились!\n'
                               'Осталось понять, какой будет минимальный возраст для поиска',
                       keyboard=back_keys.get_keyboard())
    await fsm.set_state(state=Reg.f_age_min, event=event, for_what=ForWhat.FOR_USER)


async def f_reg_age_max(event: SimpleBotEvent):
    await event.answer(message='Прекрасный выбор!\n'
                               'А максимальный?',
                       keyboard=back_keys.get_keyboard())
    await fsm.set_state(state=Reg.f_age_max, event=event, for_what=ForWhat.FOR_USER)


async def f_reg_finish(event: SimpleBotEvent):

    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    profile_id = await add_profile(vk_id=event.user_id, name=data['name'],
                                   bdate=datetime.datetime.strptime(data['bdate'], '%d.%m.%Y'), sex=data['sex'],
                                   city=data['city'], description=data['description'], geo_lat=data['geo']['latitude'],
                                   geo_long=data['geo']['longitude'])
    f_m = f_f = p1 = p2 = p3 = p4 = p5 = 0
    if 1 in data['sex_f']:
        f_f = 1
    if 2 in data['sex_f']:
        f_m = 1
    if 1 in data['purposes']:
        p1 = 1
    if 2 in data['purposes']:
        p2 = 1
    if 3 in data['purposes']:
        p3 = 1
    if 4 in data['purposes']:
        p4 = 1
    if 5 in data['purposes']:
        p5 = 1
    await add_settings(vk_id=event.user_id, age_min=data['age_min'], age_max=data['age_max'], purp1=p1, purp2=p2,
                       purp3=p3, purp4=p4, purp5=p5, find_f=f_f, find_m=f_m)
    await add_profile_photos(event.user_id, photos=data['photos'])
    await event.answer(message='Ура! Регистрация завершена\nВот так выглядит твой профиль:')
    prof = await generate_profile_forview(profile_id, event.user_id)
    await event.answer(message=prof['msg1'],
                       attachment=prof['att1'])
    await event.answer(message=prof['msg2'],
                       attachment=prof['att2'])
    await fsm.finish(event=event, for_what=ForWhat.FOR_USER)