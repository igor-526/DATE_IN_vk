async def gen_purposes():
    purposes = ['Общение', 'Флирт', 'Cоздание семьи', 'Поразвлекаться', 'Отношения']
    result = {'len': len(purposes), 'msg': ''}
    counter = 1
    for i in purposes:
        result['msg'] += f'{counter}. {i}\n'
        counter += 1
    return result
