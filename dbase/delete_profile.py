from models import Profile, Images

async def del_profile(id):
    profile = await Profile.query.where(Profile.vk_id == id).gino.first()
    photos = await Images.query.where(Images.profile == id).where(Images.description == 'profile_photo').gino.all()
    for photo in photos:
        await photo.delete()
    await profile.delete()