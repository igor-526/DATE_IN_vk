async def valid_name (name: str):
    with open(file='fixtures/obscene.txt', mode='r') as file:
        obs = file.readlines()
        for line in obs:
            if line.strip('\n') in name.lower():
                return 'obscene'
    with open(file='fixtures/name.txt', mode='r') as file:
        obs = file.readlines()
        for line in obs:
            if line.strip('\n') in name.lower():
                return 'invalid'
    if len(name) == 1:
        return 'short'
    if len(name) > 15:
        return 'long'
    return 'valid'