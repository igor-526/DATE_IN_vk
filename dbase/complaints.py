from models import Complaintlist, Images
from datetime import date
from dbase.offers import profile_pass


async def send_complaint(pr_id, to_id, cat, description, images):
    img_ids = []
    if images:
        for image in images:
            image = Images(url_vk=image['vk_url'],
                           profile_id=int(pr_id),
                           description='complaint',
                           url=image['url'])
            await image.create()
            img_ids.append(str(image.id))
    complaint = Complaintlist(cat=cat,
                              description=description,
                              images=','.join(img_ids),
                              status='new',
                              date=date.today(),
                              complain_to_id=to_id,
                              profile_id=int(pr_id))
    await complaint.create()
    if to_id:
        await profile_pass(prof_id=pr_id, offer_id=to_id)
