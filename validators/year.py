async def valid_year(year):
    try:
        int(year)
    except:
        return 'invalid'
    if 1960<int(year)<2010:
        return 'valid'
    else:
        return 'invalid'