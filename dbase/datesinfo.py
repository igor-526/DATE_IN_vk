from models import Settings
from dbase.vktoid import get_profile_id


async def dates_info(vk_id):
    prof_id = await get_profile_id(vk_id)
    settings = await Settings.query.where(Settings.id == prof_id).gino.first()
    return {'created': settings.created, 'last_usage': settings.last_usage, 'deactivated': settings.deactivated,
            'name': settings.ch_name, 'sex': settings.ch_sex, 'bdate': settings.ch_bdate}