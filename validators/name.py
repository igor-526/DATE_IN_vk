async def valid_name(name):

    obscene = ['долбоёб', 'еблан']
    c = ['1', '2', '3']

    for i in c:
        if i in name:
            return 'invalid'
    for i in obscene:
        if i in name:
            return 'obscene'
    return 'valid'