import datetime
from funcs import get_bdate_info

async def valid_bdate(bdate: str):
    try:
        datelist = bdate.split('.')
        if len(datelist) != 3:
            return 'invalid'
        date = datetime.date(year=int(datelist[2]), month=int(datelist[1]), day=int(datelist[0]))
        bdate_info = await get_bdate_info(date)
        if 14 <= bdate_info['age'] <= 60:
            return 'valid'
        else:
            return 'interval'
    except:
        return 'invalid'