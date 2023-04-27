async def valid_description (description: str):
    if len(description) >= 4000:
        return 'long'
    with open(file='fixtures/obscene.txt', mode='r') as file:
        obs = file.readlines()
        for line in obs:
            if line.strip('\n') in description.lower():
                return 'obscene'
    return 'valid'
