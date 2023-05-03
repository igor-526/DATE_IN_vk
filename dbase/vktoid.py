from models import Profile

async def get_profile_id(vk_id):
    profile = await Profile.query.where(Profile.vk_id == vk_id).gino.first()
    return profile.id
