from models import Profile, Settings, Images
from dbase.vktoid import get_profile_id
import datetime


async def upd_name(vk_id, name):
    prof_id = await get_profile_id(vk_id)
    profile = await Profile.query.where(Profile.id == prof_id).gino.first()
    settings = await Settings.query.where(Settings.id == prof_id).gino.first()
    await profile.update(name=name).apply()
    await settings.update(ch_name=datetime.datetime.now()).apply()


async def upd_bdate(vk_id, bdate):
    prof_id = await get_profile_id(vk_id)
    profile = await Profile.query.where(Profile.id == prof_id).gino.first()
    settings = await Settings.query.where(Settings.id == prof_id).gino.first()
    await profile.update(bdate=bdate).apply()
    await settings.update(ch_bdate=datetime.datetime.now()).apply()


async def upd_sex(vk_id, sex):
    prof_id = await get_profile_id(vk_id)
    profile = await Profile.query.where(Profile.id == prof_id).gino.first()
    settings = await Settings.query.where(Settings.id == prof_id).gino.first()
    await profile.update(sex=sex).apply()
    await settings.update(ch_sex=datetime.datetime.now()).apply()


async def upd_purposes(vk_id,
                       purps: list):
    prof_id = await get_profile_id(vk_id)
    settings = await Settings.query.where(Settings.id == prof_id).gino.first()
    purp1 = 1 if 1 in purps else 0
    purp2 = 1 if 2 in purps else 0
    purp3 = 1 if 3 in purps else 0
    purp4 = 1 if 4 in purps else 0
    purp5 = 1 if 5 in purps else 0
    await settings.update(purp1=purp1, purp2=purp2, purp3=purp3, purp4=purp4, purp5=purp5).apply()


async def upd_geo(vk_id, geo):
    prof_id = await get_profile_id(vk_id)
    profile = await Profile.query.where(Profile.id == prof_id).gino.first()
    await profile.update(city=geo.place.city, geo_lat=geo.coordinates.latitude,
                         geo_long=geo.coordinates.longitude).apply()


async def upd_description(vk_id, description):
    prof_id = await get_profile_id(vk_id)
    profile = await Profile.query.where(Profile.id == prof_id).gino.first()
    await profile.update(description=description).apply()


async def upd_c_photos(vk_id):
    prof_id = await get_profile_id(vk_id)
    photos = await Images.query.where(Images.profile == prof_id).where(Images.description == 'profile_photo').gino.all()
    return len(photos)


async def upd_add_photos(vk_id, photos):
    prof_id = await get_profile_id(vk_id)
    for photo in photos:
        image = Images(profile=prof_id, url=photo["url"], url_vk=photo["vk_url"], description='profile_photo')
        await image.create()


async def upd_del_photos(vk_id):
    prof_id = await get_profile_id(vk_id)
    photos = await Images.query.where(Images.profile == prof_id).where(Images.description == 'profile_photo').gino.all()
    for photo in photos:
        await photo.delete()


async def upd_sex_f(vk_id, sex_f: list):
    prof_id = await get_profile_id(vk_id)
    settings = await Settings.query.where(Settings.id == prof_id).gino.first()
    find_m = 1 if 1 in sex_f else 0
    find_f = 1 if 2 in sex_f else 0
    await settings.update(find_m=find_m, find_f=find_f).apply()


async def upd_age_f(vk_id, age_min, age_max):
    prof_id = await get_profile_id(vk_id)
    settings = await Settings.query.where(Settings.id == prof_id).gino.first()
    await settings.update(age_min=age_min, age_max=age_max).apply()


async def upd_deactivate_profile(vk_id):
    prof_id = await get_profile_id(vk_id)
    profile = await Profile.query.where(Profile.id == prof_id).gino.first()
    settings = await Settings.query.where(Settings.id == prof_id).gino.first()
    await profile.update(status='deactivated').apply()
    await settings.update(deactivated=datetime.datetime.now()).apply()


async def upd_activate_profile(vk_id):
    prof_id = await get_profile_id(vk_id)
    profile = await Profile.query.where(Profile.id == prof_id).gino.first()
    settings = await Settings.query.where(Settings.id == prof_id).gino.first()
    await profile.update(status='active').apply()
    await settings.update(deactivated=None).apply()


async def upd_delete_profile(vk_id):
    prof_id = await get_profile_id(vk_id)
    profile = await Profile.query.where(Profile.id == prof_id).gino.first()
    settings = await Settings.query.where(Settings.id == prof_id).gino.first()
    photos = await Images.query.where(Images.profile == prof_id).where(Images.description == 'profile_photo').gino.all()
    for photo in photos:
        await photo.delete()
    await settings.delete()
    await profile.delete()
