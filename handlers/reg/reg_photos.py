from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.types.objects import MessagesMessageAttachmentType
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, Reg
from keyboards import skip_keys
from funcs import f_reg_description, f_reg_geo
from vkapi import get_photos_info

reg_photo_router = DefaultRouter()


@simple_bot_message_handler(reg_photo_router, filters.PayloadFilter({"command": "back"}),
                            StateFilter(fsm=fsm, state=Reg.photo, for_what=ForWhat.FOR_USER))
async def back(event: SimpleBotEvent):
    await f_reg_geo(event)


@simple_bot_message_handler(reg_photo_router, filters.PayloadFilter({"command": "skip"}),
                            StateFilter(fsm=fsm, state=Reg.photo, for_what=ForWhat.FOR_USER))
async def skip(event: SimpleBotEvent):
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'photos': []})
    await f_reg_description(event)


@simple_bot_message_handler(reg_photo_router, filters.AttachmentTypeFilter(MessagesMessageAttachmentType.PHOTO),
                            StateFilter(fsm=fsm, state=Reg.photo, for_what=ForWhat.FOR_USER))
async def getphoto(event: SimpleBotEvent):
    photos = await get_photos_info(event.object.object.message.id)
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'photos': photos})
    await f_reg_description(event)


@simple_bot_message_handler(reg_photo_router,
                            StateFilter(fsm=fsm, state=Reg.photo, for_what=ForWhat.FOR_USER))
async def invalid(event: SimpleBotEvent):
    await event.answer(message='Я не знаю, что делать с этим сообщением\n'
                               'Пожалуйста, отправь мне просто до 3-х фотографий или нажми кнопку "Пропустить"',
                       keyboard=skip_keys.get_keyboard())