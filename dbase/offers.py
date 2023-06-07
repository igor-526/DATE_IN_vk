from models import Offerlist, Profile, Matchlist
import datetime
import requests
import config


async def get_search_profile(prof):
    offer = await Offerlist.query.where(Offerlist.profile_id == prof).where(
        Offerlist.status == 'not_offered').gino.first()
    if offer:
        return {'id':offer.offer_id, 'dist': offer.dist}
    else:
        requrl = f'{config.api_url}/do_offers/'
        params = {"id": prof,
                  "auth_token": config.api_token}
        resp = requests.post(url=requrl, json=params)
        status = resp.json()['status']
        if status == 'ready':
            offer = await Offerlist.query.where(Offerlist.profile_id == prof).where(
                Offerlist.status == 'not_offered').gino.first()
            return {'id':offer.offer_id, 'dist': offer.dist}
        elif status == 'no_profiles':
            return 'no_profiles'


async def profile_like(prof_id, offer_id):
    prof = await Profile.query.where(Profile.id == prof_id).gino.first()
    if prof.limit == 0:
        return 'limit'
    else:
        offer = await Offerlist.query.where(Offerlist.profile_id == prof_id).where(
            Offerlist.offer_id == offer_id).gino.first()
        await offer.update(status='like').apply()
        await prof.update(limit=prof.limit-1).apply()
        check_match = await Offerlist.query.where(Offerlist.profile_id == offer_id).where(
            Offerlist.offer_id == prof_id).where(Offerlist.status == 'like').gino.first()
        if check_match:
            match1 = Matchlist(profile_1_id=check_match.profile_id, profile_2_id=check_match.offer_id,
                               date=datetime.date.today(), status='not_showed')
            match2 = Matchlist(profile_1_id=check_match.offer_id, profile_2_id=check_match.profile_id,
                               date=datetime.date.today(), status='not_showed')
            await match1.create()
            await match2.create()
            return 'match'
        else:
            return 'liked'


async def profile_pass(prof_id, offer_id):
    offer = await Offerlist.query.where(Offerlist.profile_id == prof_id).where(
        Offerlist.offer_id == offer_id).gino.first()
    await offer.update(status='pass').apply()


async def clean_offerlist(prof_id):
    offers = await Offerlist.query.where(Offerlist.profile_id == prof_id).where(
        Offerlist.status=='not_offered').gino.all()
    for offer in offers:
        await offer.delete()
