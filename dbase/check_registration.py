from models import Profile

async def chk_reg(id):
    profile = await Profile.query.where(Profile.vk_id == id).gino.first()
    return profile