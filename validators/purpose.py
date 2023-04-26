async def valid_purpose(msg: str, len):
    msg = msg.replace(', ', ',').replace(' ,', ',').replace(' ', ',')
    msg = msg.split(',')
    result = []
    for i in msg:
        try:
            i = int(i)
        except: return 'invalid'
        if 1<=i<=len:
            if i not in result:
                result.append(i)
        else: return 'invalid'
    return result