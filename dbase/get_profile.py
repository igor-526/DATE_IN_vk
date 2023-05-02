from models import Profile, Settings, Images


async def get_prof_forview(id):
    profile = await Profile.query.where(Profile.id == id).gino.first()
    settings = await Settings.query.where(Profile.id == id).gino.first()
    photos = await Images.query.where(Images.profile == id).where(Images.description == 'profile_photo').gino.all()
    counter = 0
    images = []
    main_photo = None
    for photo in photos:
        counter += 1
        if counter == 1:
            main_photo = photo.url_vk
        else:
            images.append(photo.url_vk)
    purposes = []
    if settings.purp1 == 1:
        purposes.append(1)
    if settings.purp2 == 1:
        purposes.append(2)
    if settings.purp3 == 1:
        purposes.append(3)
    if settings.purp4 == 1:
        purposes.append(4)
    if settings.purp5 == 1:
        purposes.append(5)
    result = {'id': profile.id, 'name': profile.name, 'city': profile.city, 'bdate': profile.bdate,
              'description': profile.description, 'main_photo': main_photo, 'other_photos': images,
              'purposes': purposes}
    return result


async def get_prof_forsetting(vk_id):
    profile = await Profile.query.where(Profile.vk_id == vk_id).gino.first()
    settings = await Settings.query.where(Profile.id == profile.id).gino.first()
    photos = await Images.query.where(Images.profile == profile.id).where(Images.description == 'profile_photo').gino.all()
    counter = 0
    images = []
    main_photo = None
    for photo in photos:
        counter += 1
        if counter == 1:
            main_photo = photo.url_vk
        else:
            images.append(photo.url_vk)
    purposes = []
    if settings.purp1 == 1:
        purposes.append(1)
    if settings.purp2 == 1:
        purposes.append(2)
    if settings.purp3 == 1:
        purposes.append(3)
    if settings.purp4 == 1:
        purposes.append(4)
    if settings.purp5 == 1:
        purposes.append(5)
    result = {'id': profile.id, 'name': profile.name, 'city': profile.city, 'bdate': profile.bdate,
              'description': profile.description, 'main_photo': main_photo, 'other_photos': images,
              'purposes': purposes, 'sex': profile.sex, 'age_min': settings.age_min, 'age_max': settings.age_max,
              'find_m': settings.find_m, 'find_f': settings.find_f}
    return result