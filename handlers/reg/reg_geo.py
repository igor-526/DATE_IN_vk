from vkwave.bots.fsm import StateFilter, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.bots import SimpleBotEvent, DefaultRouter, simple_bot_message_handler
from FSM import fsm, Reg
from keyboards import geo_keys
from funcs import invalid, f_reg_bdate, f_reg_photo

reg_geo_router = DefaultRouter()


@simple_bot_message_handler(reg_geo_router, filters.PayloadFilter({"command": "back"}),
                            StateFilter(fsm=fsm, state=Reg.geo, for_what=ForWhat.FOR_USER))
async def back(event: SimpleBotEvent):
    await f_reg_bdate(event)


@simple_bot_message_handler(reg_geo_router,
                            StateFilter(fsm=fsm, state=Reg.geo, for_what=ForWhat.FOR_USER))
async def getgeo(event: SimpleBotEvent):
    try:
        geo = event.object.object.message.geo
        await fsm.add_data(event=event, for_what=ForWhat.FOR_USER,
                           state_data={'city': geo.place.city, 'geo': {'latitude': geo.coordinates.latitude,
                                                                       'longitude': geo.coordinates.longitude}})
        await f_reg_photo(event)
    except:
        await invalid(event, keys=geo_keys)