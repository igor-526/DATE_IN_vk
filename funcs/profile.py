from dbase import get_prof_forview
from funcs.bdate_to_info import get_bdate_info
from funcs.purposes import get_purposes_from_list


async def generate_profile_forview(id, dist):
    profile = await get_prof_forview(id)
    bdate_info = await get_bdate_info(profile["bdate"])
    msg1 = f'{profile["name"]}, {bdate_info["age"]} (id: {profile["id"]})\n' \
           f'{bdate_info["zodiac"]}, {dist} км от тебя\n' \
           f'{profile["city"]}\n\nЦели:\n'
    purposes = await get_purposes_from_list(profile['purposes'])
    for purpose in purposes:
        msg1 += f'{purpose}\n'
    msg2 = profile["description"]
    att1 = profile['main_photo']
    att2 = profile['other_photos']
    return {'msg1': msg1, 'msg2': msg2, 'att1': att1, 'att2': att2}


async def generate_profile_forsettings(id):
    profile = await get_prof_forview(id)
    bdate_info = await get_bdate_info(profile["bdate"])
    msg1 = f'{profile["name"]}, {bdate_info["age"]} (id: {profile["id"]})\n' \
           f'{bdate_info["zodiac"]}\n' \
           f'{profile["city"]}\n\nЦели:\n'
    purposes = await get_purposes_from_list(profile['purposes'])
    for purpose in purposes:
        msg1 += f'{purpose}\n'
    msg2 = profile["description"]
    att1 = profile['main_photo']
    att2 = profile['other_photos']
    return {'msg1': msg1, 'msg2': msg2, 'att1': att1, 'att2': att2}