async def gen_purposes():
    msg = ''
    counter = 1
    with open(file='fixtures/purposes.txt', mode='r') as file:
        purposes = file.readlines()
        for purpose in purposes:
            purp = purpose.strip("\n")
            msg += f'{counter}. {purp}\n'
            counter += 1
    return msg


async def get_purposes_from_list(purps: list):
    result = []
    with open(file='fixtures/purposes.txt', mode='r') as file:
        purposes = file.readlines()
        for purp in purps:
            result.append(purposes[purp-1].strip('\n'))
    return result
