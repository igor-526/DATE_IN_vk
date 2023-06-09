from models import Matchlist


async def count_matches(prof_id):
    matches = await Matchlist.query.where(Matchlist.profile_1_id == prof_id).where(
        Matchlist.status == 'not_showed').gino.all()
    return len(matches)


async def new_match(prof_id):
    match = await Matchlist.query.where(Matchlist.profile_1_id == prof_id).where(
        Matchlist.status == 'not_showed').gino.first()
    if match:
        await match.update(status='showed').apply()
        return match.profile_2_id


async def old_match(prof_id):
    matches = await Matchlist.query.where(Matchlist.profile_1_id == prof_id).where(
        Matchlist.status == 'showed').gino.all()
    result = [match.profile_2_id for match in matches]
    return result