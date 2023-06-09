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
                      geo_lat=geo_lat, geo_long=geo_long, limit=50)
    await profile.create()
    return profile.id


async def add_settings(pr_id: int,
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
    settings = Settings(profile_id=pr_id, age_min=age_min, age_max=age_max, find_m=find_m, find_f=find_f, purp1=purp1,
                        purp2=purp2, purp3=purp3, purp4=purp4, purp5=purp5, created=date.today(),
                        last_usage=datetime.now(), km_limit=15)
    await settings.create()


async def add_profile_photos(pr_id: int,
                             photos: list):
    for photo in photos:
        image = Images(profile_id=pr_id, url=photo["url"], url_vk=photo["vk_url"], description='profile_photo')
        await image.create()


async def add_vk_id(tg_id: int,
                    vk_id: int):
    profile = await Profile.query.where(Profile.tg_id == tg_id).gino.first()
    await profile.update(vk_id=vk_id).apply()
