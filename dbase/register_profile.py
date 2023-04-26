from models import Profile, Images


async def add_profile(vk_id: int,
                      name: str,
                      age: int,
                      sex: int,
                      city_id: int,
                      city_title: str,
                      description,
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
    profile = Profile(vk_id=vk_id, name=name, age=age, sex=sex, city_id=city_id, city_title=city_title,
                      description=description, age_min=age_min, age_max=age_max, find_m=find_m, find_f=find_f,
                      purp1=purp1, purp2=purp2, purp3=purp3, purp4=purp4, purp5=purp5)
    await profile.create()


async def add_images(id: int, urls: list):
    for url in urls:
        image = Images(profile=id, url=url, description='profile_photo')
        await image.create()
 

async def reg_profile(vk_id, data):
    find_m = 0
    find_f = 0
    purp1 = 0
    purp2 = 0
    purp3 = 0
    purp4 = 0
    purp5 = 0
    if data['sexf'] == 1:
        find_f = 1
    elif data['sexf'] == 2:
        find_m = 1
    elif data['sexf'] == 3:
        find_f = 1
        find_m = 1
    if 1 in data['purposes']:
        purp1 = 1
    if 2 in data['purposes']:
        purp2 = 1
    if 3 in data['purposes']:
        purp3 = 1
    if 4 in data['purposes']:
        purp4 = 1
    if 5 in data['purposes']:
        purp5 = 1
    await add_profile(vk_id=int(vk_id),
                      name=str(data['name']),
                      age=int(data['age']),
                      sex=int(data['sex']),
                      city_id=int(data['city_id']),
                      city_title=str(data['city_title']),
                      description=data['description'],
                      age_min=int(data['age_min']),
                      age_max=int(data['age_max']),
                      find_m=find_m,
                      find_f=find_f,
                      purp1=purp1,
                      purp2=purp2,
                      purp3=purp3,
                      purp4=purp4,
                      purp5=purp5
                      )
    await add_images(id=vk_id, urls=data['photos'])