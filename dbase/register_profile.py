from datetime import date, datetime
from models import Profile, Settings, Images


async def add_profile(vk_id: int,
                      name: str,
                      bdate: date,
                      sex: int,
                      city: str,
                      geo_lat: float,
                      geo_long: float,
                      description: str):
    profile = Profile(vk_id=vk_id, name=name, bdate=bdate, sex=sex, city=city, description=description, status='active',
                      geo_lat=geo_lat, geo_long=geo_long)
    await profile.create()
    return profile.id


async def add_settings(vk_id: int,
                       age_min: int,
                       age_max: int,
                       find_m: int,
                       find_f: int,
                       purp1: int,
                       purp2: int,
                       purp3: int,
                       purp4: int,
                       purp5: int,
                       ):
    profile = await Profile.query.where(Profile.vk_id == vk_id).gino.first()
    settings = Settings(id = profile.id, age_min=age_min, age_max=age_max, find_m=find_m, find_f=find_f, purp1=purp1,
                        purp2=purp2, purp3=purp3, purp4=purp4, purp5=purp5, created=date.today(),
                        last_usage=datetime.now())
    await settings.create()


async def add_profile_photos(vk_id: int,
                             photos: list):
    profile = await Profile.query.where(Profile.vk_id == vk_id).gino.first()
    for photo in photos:
        image = Images(profile=profile.id, url=photo["url"], url_vk=photo["vk_url"], description='profile_photo')
        await image.create()
