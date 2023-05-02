async def valid_age(age, min_age):
    try:
        age = int(age)
        if min_age:
            min_age = int(min_age)
    except:
        return 'invalid'
    if min_age:
        if min_age > age:
            return 'more_min'
    if age > 60:
        return 'too_old'
    elif 1 <= age < 14:
        return 'too_small'
    elif age < 1:
        return 'invalid'
    return 'valid'