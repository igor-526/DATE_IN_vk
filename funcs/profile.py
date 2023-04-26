from bot import bot
from vkwave.bots.utils.uploaders import PhotoUploader
from dbase import get_prof
from pprint import pprint


async def gen_profile(id):
    data = await get_prof(id)
    result = {'msg1': '', 'msg2': data['profile']['description'], 'att1': None, 'att2': None}
    result['msg1'] = f'{data["profile"]["name"]}, {data["profile"]["age"]} (id {data["profile"]["id"]})\n' \
                     f'{data["profile"]["city"]}\n\nЦели:\n'
    if 1 in data['settings']['purposes']: result['msg1'] += '&#10145;общение\n'
    if 2 in data['settings']['purposes']: result['msg1'] += '&#10145;флирт\n'
    if 3 in data['settings']['purposes']: result['msg1'] += '&#10145;создание семьи\n'
    if 4 in data['settings']['purposes']: result['msg1'] += '&#10145;поразвлекаться\n'
    if 5 in data['settings']['purposes']: result['msg1'] += '&#10145;отношения\n'
    if data['main_photo']:
        result['att1'] = await PhotoUploader(bot.api_context).get_attachment_from_link(peer_id=id, link=data['main_photo'])
    if len(data['other_photos']) != 0:
        result['att2'] = await PhotoUploader(bot.api_context).get_attachments_from_links(peer_id=id,
                                                                                     links=data['other_photos'])
    return result


async def gen_profile_settings(id):
    data = await get_prof(id)
    result = {'msg1': '', 'msg2': f'Описание: {data["profile"]["description"]}\nОст. фото:', 'att1': None, 'att2': None}
    if data['main_photo']:
        result['att1'] = await PhotoUploader(bot.api_context).get_attachment_from_link(peer_id=id, link=data['main_photo'])
    if len(data['other_photos']) != 0:
        result['att2'] = await PhotoUploader(bot.api_context).get_attachments_from_links(peer_id=id,
                                                                                         links=data['other_photos'])
    result['msg1'] = f'Имя: {data["profile"]["name"]}\n' \
                     f'Возраст: {data["profile"]["age"]}\n' \
                     f'Город: {data["profile"]["city"]}\n' \
                     f'Пол: {data["profile"]["sex"]}\n' \
                     f'ID: {data["profile"]["id"]}\n\nЦели:\n'
    if 1 in data['settings']['purposes']: result['msg1'] += '&#10145;общение\n'
    if 2 in data['settings']['purposes']: result['msg1'] += '&#10145;флирт\n'
    if 3 in data['settings']['purposes']: result['msg1'] += '&#10145;создание семьи\n'
    if 4 in data['settings']['purposes']: result['msg1'] += '&#10145;поразвлекаться\n'
    if 5 in data['settings']['purposes']: result['msg1'] += '&#10145;отношения\n'
    result['msg1'] += 'Ищем: '
    if data['settings']['find_f'] and data['settings']['find_m']: result['msg1'] += 'мужчин и девушек\n'
    elif data['settings']['find_f']: result['msg1'] += 'только девушек\n'
    elif data['settings']['find_m']: result['msg1'] += 'только мужчин\n'
    result['msg1'] += f'От {data["settings"]["age_min"]} до {data["settings"]["age_max"]} лет\n' \
                      f'Главная фотография:'
    return result