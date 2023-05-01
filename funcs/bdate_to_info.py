import datetime


async def get_bdate_info(bdate):
    delta = datetime.date.today() - bdate
    age = int(delta.days//365.25)
    zodiac = None
    if datetime.date(month=3, day=21, year=2000) <= bdate.replace(year=2000) <= datetime.date(month=4, day=19, year=2000):
        zodiac = 'овен'
    elif datetime.date(month=4, day=20, year=2000) <= bdate.replace(year=2000) <= datetime.date(month=5, day=20, year=2000):
        zodiac = 'телец'
    elif datetime.date(month=5, day=21, year=2000) <= bdate.replace(year=2000) <= datetime.date(month=6, day=21, year=2000):
        zodiac = 'близнецы'
    elif datetime.date(month=6, day=22, year=2000) <= bdate.replace(year=2000) <= datetime.date(month=7, day=22, year=2000):
        zodiac = 'рак'
    elif datetime.date(month=7, day=23, year=2000) <= bdate.replace(year=2000) <= datetime.date(month=8, day=22, year=2000):
        zodiac = 'лев'
    elif datetime.date(month=8, day=23, year=2000) <= bdate.replace(year=2000) <= datetime.date(month=9, day=22, year=2000):
        zodiac = 'дева'
    elif datetime.date(month=9, day=23, year=2000) <= bdate.replace(year=2000) <= datetime.date(month=10, day=23, year=2000):
        zodiac = 'весы'
    elif datetime.date(month=10, day=24, year=2000) <= bdate.replace(year=2000) <= datetime.date(month=11, day=24, year=2000):
        zodiac = 'скорпион'
    elif datetime.date(month=11, day=23, year=2000) <= bdate.replace(year=2000) <= datetime.date(month=12, day=21, year=2000):
        zodiac = 'стрелец'
    elif datetime.date(month=12, day=22, year=2000) <= bdate.replace(year=2000) <= datetime.date(month=12, day=31, year=2000):
        zodiac = 'козерог'
    elif datetime.date(month=1, day=1, year=2000) <= bdate.replace(year=2000) <= datetime.date(month=1, day=20, year=2000):
        zodiac = 'козерог'
    elif datetime.date(month=1, day=21, year=2000) <= bdate.replace(year=2000) <= datetime.date(month=2, day=18, year=2000):
        zodiac = 'водолей'
    elif datetime.date(month=2, day=19, year=2000) <= bdate.replace(year=2000) <= datetime.date(month=3, day=20, year=2000):
        zodiac = 'рыбы'
    return {'age': age, 'zodiac': zodiac}