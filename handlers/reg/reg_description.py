from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, Reg
from funcs import f_reg_photo, f_reg_purposes
from validators import valid_description

reg_description_router = DefaultRouter()


@simple_bot_message_handler(reg_description_router, filters.PayloadFilter({"command": "back"}),
                            StateFilter(fsm=fsm, state=Reg.description, for_what=ForWhat.FOR_USER))
async def back(event: SimpleBotEvent):
    await f_reg_photo(event)


@simple_bot_message_handler(reg_description_router, filters.PayloadFilter({"command": "skip"}),
                            StateFilter(fsm=fsm, state=Reg.description, for_what=ForWhat.FOR_USER))
async def skip(event: SimpleBotEvent):
    await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'description': None})
    await f_reg_purposes(event)


@simple_bot_message_handler(reg_description_router,
                            StateFilter(fsm=fsm, state=Reg.description, for_what=ForWhat.FOR_USER))
async def valid(event: SimpleBotEvent):
    validator = await valid_description(event.text)
    if validator == 'valid':
        await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'description': event.text})
        await f_reg_purposes(event)
    elif validator == 'obscene':
        await event.answer(message="Мы против нецензурной лексики\n"
                                   "фильтр мог сработать ошибочно, пока что оставим так, но твоё описание бует "
                                   "отправлено на модерацию")
        await fsm.add_data(event=event, for_what=ForWhat.FOR_USER, state_data={'description': event.text})
        await f_reg_purposes(event)
    elif validator == 'long':
        return "Слишком длинное описание\n" \
               "К сожалению, это не наше ограничение, а мессенджеров"
