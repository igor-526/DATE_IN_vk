from dbase import get_prof_forview, get_prof_forsetting, get_description
from funcs.bdate_to_info import get_bdate_info
from funcs.purposes import get_purposes_from_list


async def generate_profile_forview(id, dist):
    profile = await get_prof_forview(id)
    bdate_info = await get_bdate_info(profile["bdate"])
    msg = f'{profile["name"]}, {bdate_info["age"]} (&#127380;{profile["id"]})\n' \
           f'{dist} км от тебя\n' \
           f'{profile["city"]}\n\nЦели:\n'
    purposes = await get_purposes_from_list(profile['purposes'])
    for purpose in purposes:
        msg += f'&#10004;{purpose}\n'
    att = profile['main_photo']
    return {'msg': msg, 'att': att}


async def generate_profile_forsettings(vk_id):
    profile = await get_prof_forsetting(vk_id)
    if profile["find_f"] == 1 and profile["find_m"] == 1:
        findsex = 'девушек и мужчин'
    elif profile["find_f"] == 1:
        findsex = 'только девушек'
    elif profile["find_m"] == 1:
        findsex = 'только мужчин'
    msg1 = f'&#127380;{profile["id"]}\n' \
           f'Имя: {profile["name"]}\n' \
           f'Дата рождения: {profile["bdate"]}\n' \
           f'Город: {profile["city"]}\n' \
           f'Пол: {"мужской" if profile["sex"] == 2 else "женский"}\n' \
           f'Вы  ищете: {findsex}\n' \
           f'От {profile["age_min"]} до {profile["age_max"]} лет\n' \
           f'Ваши цели:\n'
    purposes = await get_purposes_from_list(profile['purposes'])
    for purpose in purposes:
        msg1 += f'&#10004;{purpose}\n'
    msg1 += '\nОсновная фотография:'
    msg2 = f'Описание: {profile["description"]}\n' \
           f'Ост. фотографии:'
    att1 = profile['main_photo']
    att2 = profile['other_photos']
    return {'msg1': msg1, 'msg2': msg2, 'att1': att1, 'att2': att2}


async def generate_profile_description(pr_id):
    description = await get_description(pr_id)
    bdate_info = await get_bdate_info(description["bdate"])
    msg = ''
    msg += f'{description["description"]}\n\n' if description["description"] else ''
    msg += f'\U0001F4CF {description["height"]} см\n' if description["height"] else ''
    msg += f'\U0001F4BC {description["busy"]}\n' if description["busy"] else ''
    msg += f'\U0001F466 {description["children"]}\n' if description["children"] else ''
    msg += f'\U0001F320 {bdate_info["zodiac"]}\n'
    msg += f'\U0001F552 {description["hobby"]}\n' if description["hobby"] else ''
    msg += f'\U0001F6AB {description["habits"]}\n' if description["habits"] else ''
    msg += f'\U0001F436 {description["animals"]}' if description["animals"] else ''
    return msg