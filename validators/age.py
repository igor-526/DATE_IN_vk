async def valid_age(age, min_age):
    try:
        age = int(age)
        if min_age: min_age=int(min_age)
    except:
        return 'invalid'
    if age > 99: return 'too_old'
    if age < 1: return 'invalid'
    if min_age:
        if min_age > age: return 'more_min'
    return 'valid'