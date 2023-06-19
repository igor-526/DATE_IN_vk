from models import Profile, Settings, Images


async def get_prof_forview(pr_id):
    profile = await Profile.query.where(Profile.id == pr_id).gino.first()
    settings = await Settings.query.where(Settings.profile_id == pr_id).gino.first()
    photo = await Images.query.where(Images.profile_id == pr_id).where(Images.description == 'profile_photo').gino.first()
    main_photo = photo.url_vk if photo else None
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
    cont_vk = f'https://vk.com/id{profile.vk_id}' if profile.vk_id else None
    cont_tg = f'https://t.me/{profile.tg_nick}' if profile.tg_nick else None
    result = {'id': profile.id, 'name': profile.name, 'city': profile.city, 'bdate': profile.bdate,
              'main_photo': main_photo, 'purposes': purposes, 'cont_vk': cont_vk, 'cont_tg': cont_tg}
    return result


async def get_prof_forsetting(pr_id):
    profile = await Profile.query.where(Profile.id == pr_id).gino.first()
    settings = await Settings.query.where(Settings.profile_id == profile.id).gino.first()
    photos = await Images.query.where(Images.profile_id == profile.id).where(
        Images.description == 'profile_photo').order_by('id').gino.all()
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
              'find_m': settings.find_m, 'find_f': settings.find_f, 'height': profile.height, 'habits': profile.habits,
              'children': profile.children, 'busy': profile.busy, 'hobby': profile.hobby, 'animals': profile.animals,
              'dist': settings.km_limit}
    return result


async def get_photos(pr_id):
    photos = await Images.query.where(Images.profile_id == pr_id).where(
        Images.description == 'profile_photo').order_by('id').gino.all()
    result = []
    for photo in photos:
        result.append(photo.url_vk)
    return result[1:]


async def get_description(pr_id):
    profile = await Profile.query.where(Profile.id == pr_id).gino.first()
    result = {'description': profile.description, 'height': profile.height, 'habits': profile.habits,
              'children': profile.children, 'busy': profile.busy, 'hobby': profile.hobby, 'animals': profile.animals,
              'bdate': profile.bdate}
    return result
