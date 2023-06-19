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
                       code_keys)
from vkwave.bots.fsm import ForWhat
from funcs import gen_purposes
from funcs.profile_settings import f_ch_d
from dbase import add_profile, add_settings, add_profile_photos
import datetime
from aiogram import Bot
from config import tg_bot_token
from random import randint


async def invalid(event: SimpleBotEvent, keys):
    await event.answer(message="Я не понимаю &#128532;\n" \
                               "Пожалуйста, выбери действие на клавиатуре",
                       keyboard=keys.get_keyboard())


async def start_registration(event: SimpleBotEvent):
    await event.answer(message="\U00002757 ВНИМАНИЕ \U00002757 \n"
                               "Продолжая регистрацию, ты даёшь своё согласие на обработку персональных данных\n"
                               "Ознакомиться с ней можно здесь datein.ru/privacy\n"
                               "При возникновении какой-нибудь трудной ситуации, оставь пожалуйста свой репорт о "
                               "работе бота, используя команду /report. Ты можешь помочь нам стать лучше!")
    await event.answer(message="Подскажи, ты используешь DATE IN в Telegram?",
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
                           "Я её никому не покажу. Только возраст и знак зодиака!",
                           keyboard=back_keys.get_keyboard())
        await fsm.set_state(state=Reg.bdate_manual, event=event, for_what=ForWhat.FOR_USER)
    elif len(data['vk']['bdate'].split('.')) == 2:
        await event.answer("Записал &#128521;\n"
                           "Вижу твой день рождения! Но мне нужен ещё и год\n"
                           "Напиши мне его, пожалуйста, в формате 'ГГГГ'\n"
                           "Я её никому не покажу. Только возраст и знак зодиака!",
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
                                   f'Ты же {"парень" if sex==2 else "девушка"}?\n'
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
                               'Это необходимо для того, чтобы подбирать тебе анкеты поближе',
                       keyboard=geo_keys.get_keyboard())
    await fsm.set_state(state=Reg.geo, event=event, for_what=ForWhat.FOR_USER)


async def f_reg_photo(event: SimpleBotEvent):
    await event.answer(message='Супер! Отправь мне фотографии, которые '
                               'будешь гордо демонстрировать другим пользователям сервиса\n'
                               'Если хочется пользоваться без фотографий (что мы очень не рекомендуем) или '
                               'отправить их потом, нажми кнопку "Пропустить"',
                       keyboard=skip_keys.get_keyboard())
    await fsm.set_state(state=Reg.photo, event=event, for_what=ForWhat.FOR_USER)


async def f_reg_description(event: SimpleBotEvent):
    await event.answer(message="Отлично! Почти последний шаг - напиши мне какой-нибудь текст, который заинтересует "
                               "любого и заставит нажать кнопку лайка!\n"
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
    await event.answer(message='С твоим профилем закончили!\nДавай теперь настроим поиск\n'
                               'Тут гораздо меньше')
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
    await event.answer("Завершение регистрации")
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    pr_id = await add_profile(vk_id=event.user_id, name=data['name'],
                                   bdate=datetime.datetime.strptime(data['bdate'], '%d.%m.%Y'), sex=data['sex'],
                                   city=data['city'], description=data['description'], geo_lat=data['geo']['latitude'],
                                   geo_long=data['geo']['longitude'])
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'pr_id': pr_id})
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
    await add_settings(pr_id, age_min=data['age_min'], age_max=data['age_max'], purp1=p1, purp2=p2,
                       purp3=p3, purp4=p4, purp5=p5, find_f=f_f, find_m=f_m)
    await add_profile_photos(pr_id, photos=data['photos'])
    await event.answer(message="Ура! Всё получилось!\n"
                               "Эти команды тебе смогут помочь в дальнейшем:\n"
                               "/help - помощь\n"
                               "/rules - правила использования сервиса\n"
                               "/menu - выйти в главное меню\n"
                               "/reset - перезагрузить бота\n"
                               "/report - оставить репорт о работе бота")
    await f_ch_d(event)


async def send_code(event: SimpleBotEvent, tg_id):
    bot = Bot(token=tg_bot_token)
    code = randint(10000, 99999)
    await bot.send_message(chat_id=tg_id, text=f'Код для входа в DATE IN в ВК: {code}')
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'code': code})
    await event.answer(message='Отправил тебе в telegram пятизначный код. Отправь мне его',
                       keyboard=code_keys.get_keyboard())
    await fsm.set_state(state=Reg.tg_code, event=event, for_what=ForWhat.FOR_USER)
