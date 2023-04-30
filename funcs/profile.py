from dbase import get_prof_forview
from pprint import pprint
from bot import bot
from vkwave.bots.utils.uploaders import PhotoUploader
from vkwave.types.objects import PhotosPhoto
img = PhotosPhoto()

async def generate_profile_forview(id, vk_id):
    profile = await get_prof_forview(id)
    pprint(profile)
    msg1 = f'{profile["name"]}, {profile["age"]} (id: {profile["id"]})\n' \
           f'ЗЗ, <x> км от тебя\n' \
           f'{profile["city"]}\n\nЦели:\n'
    msg2 = f'{profile["description"]}'
    att1 = await PhotoUploader(api_context=bot.api_context).get_attachment_from_link(peer_id=vk_id,
                                                                                     link=profile['main_photo'])
    att2 = await PhotoUploader(api_context=bot.api_context).get_attachments_from_links(peer_id=vk_id,
                                                                                       links=profile['other_photos'])
    await PhotoUploader(api_context=bot.api_context).attachment_name([PhotosPhoto])
    return {'msg1': msg1, 'msg2': msg2, 'att1': att1, 'att2': att2}