from models import Offerlist
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
    offer = await Offerlist.query.where(Offerlist.profile_id == prof_id).where(
        Offerlist.offer_id == offer_id).gino.first()
    await offer.update(status='like').apply()


async def profile_pass(prof_id, offer_id):
    offer = await Offerlist.query.where(Offerlist.profile_id == prof_id).where(
        Offerlist.offer_id == offer_id).gino.first()
    await offer.update(status='pass').apply()


async def clean_offerlist(prof_id):
    offers = await Offerlist.query.where(Offerlist.profile_id == prof_id).where(
        Offerlist.status=='not_offered').gino.all()
    for offer in offers:
        await offer.delete()
