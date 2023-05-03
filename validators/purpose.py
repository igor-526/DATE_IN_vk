async def valid_purpose(msg: str):
    msg = msg.replace(', ', ',').replace(' ,', ',').replace(' ', ',')
    msg = msg.split(',')
    result = []
    for i in msg:
        try:
            i = int(i)
        except:
            return 'invalid'
        if 1 <= i <= 5:
            if i not in result:
                result.append(i)
        else:
            return 'invalid'
    return result
