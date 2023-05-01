from dbase import get_prof_forview
from pprint import pprint
from funcs.bdate_to_info import get_bdate_info


async def generate_profile_forview(id, vk_id):
    profile = await get_prof_forview(id)
    pprint(profile)
    bdate_info = await get_bdate_info(profile["bdate"])
    msg1 = f'{profile["name"]}, {bdate_info["age"]} (id: {profile["id"]})\n' \
           f'{bdate_info["zodiac"]}, <x> км от тебя\n' \
           f'{profile["city"]}\n\nЦели:\n'
    msg2 = f'{profile["description"]}'
    att1 = profile['main_photo']
    att2 = profile['other_photos']
    return {'msg1': msg1, 'msg2': msg2, 'att1': att1, 'att2': att2}
