from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from vkwave.types.objects import MessagesMessageAttachmentType
from FSM import fsm, Profile
from keyboards import prof_set_keys
from vkapi import get_photos_info
from dbase import upd_add_photos, upd_del_photos, upd_c_photos

prs_photos_router = DefaultRouter()


@simple_bot_message_handler(prs_photos_router, filters.PayloadFilter({"command": "cancel"}),
                            StateFilter(fsm=fsm, state=Profile.add_photos, for_what=ForWhat.FOR_USER))
async def cancel_add(event: SimpleBotEvent):
    await event.answer("Выберите действие:",
                       keyboard=prof_set_keys.get_keyboard())
    await fsm.set_state(state=Profile.show, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(prs_photos_router, filters.PayloadFilter({"command": "no"}),
                            StateFilter(fsm=fsm, state=Profile.del_photos, for_what=ForWhat.FOR_USER))
async def cancel_del(event: SimpleBotEvent):
    await event.answer("Выберите действие:",
                       keyboard=prof_set_keys.get_keyboard())
    await fsm.set_state(state=Profile.show, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(prs_photos_router, filters.PayloadFilter({"command": "yes"}),
                            StateFilter(fsm=fsm, state=Profile.del_photos, for_what=ForWhat.FOR_USER))
async def deletephotos(event: SimpleBotEvent):
    await upd_del_photos(event.user_id)
    await event.answer(message="Удалил. Теперь ты можешь добавить 11 фотографий для профиля!\n"
                               "Выберите действие:",
                       keyboard=prof_set_keys.get_keyboard())
    await fsm.set_state(state=Profile.show, event=event, for_what=ForWhat.FOR_USER)


@simple_bot_message_handler(prs_photos_router, filters.AttachmentTypeFilter(MessagesMessageAttachmentType.PHOTO),
                            StateFilter(fsm=fsm, state=Profile.add_photos, for_what=ForWhat.FOR_USER))
async def addphotos(event: SimpleBotEvent):
    photos = await get_photos_info(event.object.object.message.id)
    count = await upd_c_photos(event.user_id)
    if len(photos) > (11-count):
        photos = photos[0:(11-count)]
    await upd_add_photos(event.user_id, photos)
    await event.answer(message='Прекрасные фотографии! Добавил!\n'
                               'Выберите действие:',
                       keyboard=prof_set_keys.get_keyboard())
    await fsm.set_state(state=Profile.show, event=event, for_what=ForWhat.FOR_USER)