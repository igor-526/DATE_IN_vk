from FSM import (fsm,
                 Profile)
from vkwave.bots import SimpleBotEvent
from keyboards import cancel_keys, sex_keys, geocancel_keys, yesno_keys, sexf_keys
from vkwave.bots.fsm import ForWhat
from dbase import dates_info, upd_c_photos
from funcs import gen_purposes


async def f_ch_name(event: SimpleBotEvent):
    ch_date = await dates_info(event.user_id)
    if not ch_date['name']:
        await event.answer('Введи имя, на которое хочешь поменять\n'
                           'Но учти, что делать это можно только один раз!',
                           keyboard=cancel_keys.get_keyboard())
        await fsm.set_state(state=Profile.name, event=event, for_what=ForWhat.FOR_USER)
    else:
        await event.answer(message=f'Вы уже меняли имя {ch_date["name"].strftime("%d.%m")}\n'
                                   f'Если есть необходимость всё-таки его поменять, обратитесь через репорт в главном '
                                   f'меню')


async def f_ch_bdate(event: SimpleBotEvent):
    ch_date = await dates_info(event.user_id)
    if not ch_date['bdate']:
        await event.answer('Введи свою дату рождения в формате ДД.ММ.ГГГГ\n'
                           'Но учти, что делать это можно только один раз!',
                           keyboard=cancel_keys.get_keyboard())
        await fsm.set_state(state=Profile.bdate, event=event, for_what=ForWhat.FOR_USER)
    else:
        await event.answer(message=f'Вы уже меняли дату рождения {ch_date["name"].strftime("%d.%m")}\n'
                                   f'Если есть необходимость всё-таки её поменять, обратитесь через репорт в главном '
                                   f'меню')


async def f_ch_sex(event: SimpleBotEvent):
    ch_date = await dates_info(event.user_id)
    if not ch_date['sex']:
        await event.answer('Кто ты?\n'
                           'Но учти, что делать это можно только один раз!',
                           keyboard=sex_keys.get_keyboard())
        await fsm.set_state(state=Profile.sex, event=event, for_what=ForWhat.FOR_USER)
    else:
        await event.answer(message=f'Вы уже меняли пол {ch_date["sex"].strftime("%d.%m")}\n'
                                   f'Если есть необходимость всё-таки поменять пол, обратитесь через репорт в главном '
                                   f'меню')


async def f_ch_purposes(event: SimpleBotEvent):
    msg = 'Пожалуйста, перечислите через запятую или пробел номера целей\n' \
          'Менять их можно сколько угодно раз!\n\n'
    msg += await gen_purposes()
    await event.answer(message=msg, keyboard=cancel_keys.get_keyboard())
    await fsm.set_state(state=Profile.purposes, event=event, for_what=ForWhat.FOR_USER)


async def f_ch_geo(event: SimpleBotEvent):
    await event.answer(message="Отправьте мне своё местоположение (можно примерное), чтобы я смог подбирать профили "
                               "сначала поближе!",
                       keyboard=geocancel_keys.get_keyboard())
    await fsm.set_state(state=Profile.geo, event=event, for_what=ForWhat.FOR_USER)


async def f_ch_description(event: SimpleBotEvent):
    await event.answer(message="Напиши мне самое лучшее описание профиля на свете!",
                       keyboard=cancel_keys.get_keyboard())
    await fsm.set_state(state=Profile.description, event=event, for_what=ForWhat.FOR_USER)


async def f_ch_del_photos(event: SimpleBotEvent):
    await event.answer(message="Функция удалит все твои фотографии профиля, но ты потом сможешь добавить их снова!\n"
                               "Уверены?",
                       keyboard=yesno_keys.get_keyboard())
    await fsm.set_state(state=Profile.del_photos, event=event, for_what=ForWhat.FOR_USER)


async def f_ch_add_photos(event: SimpleBotEvent):
    count = await upd_c_photos(event.user_id)
    if count == 11:
        await event.answer(message='У тебя уже 11 фотографий!\n'
                                   'К сожалению, больше нельзя. Для начала нужно удалить фотографии')
    else:
        await event.answer(message=f'Отправь мне свои самые лучшие фотографии!\n'
                                   f'(Макс. {11-count}. остальные не смогу добавить :( )',
                           keyboard=cancel_keys.get_keyboard())
        await fsm.set_state(state=Profile.add_photos, event=event, for_what=ForWhat.FOR_USER)


async def f_ch_age_f(event: SimpleBotEvent):
    await event.answer(message="Введите минимальный возраст для поиска:",
                       keyboard=cancel_keys.get_keyboard())
    await fsm.set_state(state=Profile.age_min, event=event, for_what=ForWhat.FOR_USER)


async def f_ch_sex_f(event: SimpleBotEvent):
    await event.answer(message="Кого будем искать?",
                       keyboard=sexf_keys.get_keyboard())
    await fsm.set_state(state=Profile.sex_f, event=event, for_what=ForWhat.FOR_USER)


async def f_ch_delete(event: SimpleBotEvent):
    await event.answer(message="В течение недели ты сможешь восстановить профиль, после чего он будет окончательно "
                               "удалён. Продолжить?",
                       keyboard=yesno_keys.get_keyboard())
    await fsm.set_state(state=Profile.delete, event=event, for_what=ForWhat.FOR_USER)