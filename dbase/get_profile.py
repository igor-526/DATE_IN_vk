from models import Profile, Images


async def get_prof(id):
    profile = await Profile.query.where(Profile.vk_id == id).gino.first()
    result = {'profile': {}, 'settings': {'purposes':[]}, 'main_photo': None, 'other_photos': []}
    result['profile']['id'] = profile.id
    result['profile']['name'] = profile.name
    result['profile']['age'] = profile.age
    if profile.sex == 2:
        result['profile']['sex'] = 'Мужской'
    if profile.sex == 1:
        result['profile']['sex'] = 'Женский'
    result['profile']['city'] = profile.city_title
    result['profile']['description'] = profile.description
    result['settings']['age_min'] = profile.age_min
    result['settings']['age_max'] = profile.age_max
    result['settings']['find_m'] = profile.find_m
    result['settings']['find_f'] = profile.find_f
    if profile.purp1: result['settings']['purposes'].append(1)
    if profile.purp2: result['settings']['purposes'].append(2)
    if profile.purp3: result['settings']['purposes'].append(3)
    if profile.purp4: result['settings']['purposes'].append(4)
    if profile.purp5: result['settings']['purposes'].append(5)
    photos = await Images.query.where(Images.profile == id).where(Images.description == 'profile_photo').gino.all()
    counter = 0
    for photo in photos:
        counter += 1
        if counter == 12: break
        if counter == 1: result['main_photo'] = photo.url
        else: result['other_photos'].append(photo.url)
    return result
