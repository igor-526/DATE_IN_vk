from FSM import fsm
from vkwave.bots import SimpleBotEvent
from vkwave.bots.fsm import ForWhat
from funcs import generate_profile_forview
from dbase import new_match, old_match
from keyboards import match_in_keys, nomatch_keys, oldmatch_keys, oldnomatch_keys
from FSM import Matches


async def show_new_match(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    match = await new_match(data['pr_id'])
    if match:
        prof = await generate_profile_forview(match)
        keyss = await match_in_keys(prof['contacts'])
        await event.answer(message=prof['msg'],
                           attachment=prof['att'],
                           keyboard=keyss.get_keyboard())
    else:
        await event.answer(message='Новых мэтчей пока нет\n'
                                   'Но ты можешь отправиться на поиски за новыми или посмотреть старые!',
                           keyboard=nomatch_keys.get_keyboard())
    await fsm.set_state(state=Matches.new_matches, event=event, for_what=ForWhat.FOR_USER)


async def next_old_match(event: SimpleBotEvent):
    try:
        data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
        cursor = data['old_matches']['cursor']+1
        matches = data['old_matches']['matches']
        await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={
            'old_matches': {'matches': matches, 'cursor': cursor}})
        prof = await generate_profile_forview(matches[cursor])
        keyss = await match_in_keys(prof['contacts'])
        await event.answer(message=prof['msg'],
                           attachment=prof['att'],
                           keyboard=keyss.get_keyboard())
    except IndexError:
        await event.answer(message='Больше нет\n'
                                   'Давайте лучше отправимся за поиском новых пар!',
                           keyboard=oldnomatch_keys.get_keyboard())


async def prev_old_match(event: SimpleBotEvent):
    try:
        data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
        cursor = data['old_matches']['cursor'] - 1
        matches = data['old_matches']['matches']
        await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={
            'old_matches': {'matches': matches, 'cursor': cursor}})
        prof = await generate_profile_forview(matches[cursor])
        keyss = await match_in_keys(prof['contacts'])
        await event.answer(message=prof['msg'],
                           attachment=prof['att'],
                           keyboard=keyss.get_keyboard())
    except IndexError:
        await event.answer(message='Больше нет\n'
                                   'Давайте лучше отправимся за поиском новых пар!',
                           keyboard=oldnomatch_keys.get_keyboard())


async def show_old_match(event: SimpleBotEvent):
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    matches = await old_match(data['pr_id'])
    if len(matches) == 0:
        await event.answer(message='У вас пока нет ни одной пары. Отправляйтесь скорее за новыми!')
    else:
        await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={
            'old_matches': {'matches': matches, 'cursor': -1}})
        await event.answer(message='Секунду..',
                           keyboard=oldmatch_keys.get_keyboard())
        await fsm.set_state(state=Matches.old_matches, event=event, for_what=ForWhat.FOR_USER)
        await next_old_match(event)
