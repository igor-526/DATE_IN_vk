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
