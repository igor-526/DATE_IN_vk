async def valid_description (description):
    with open(file='fixtures/obscene.txt', mode='r') as file:
        obs = file.readlines()
        for line in obs:
            if line.strip('\n') in description:
                return 'invalid'
        return 'valid'