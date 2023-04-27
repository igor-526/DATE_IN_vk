from vkwave.bots.fsm import StateFilter, ANY_STATE, ForWhat
from vkwave.bots.core.dispatching import filters
from vkwave.types.objects import MessagesMessageAttachmentType
from vkwave.bots import (SimpleBotEvent,
                         DefaultRouter,
                         simple_bot_message_handler,
                         Keyboard)
from FSM import (fsm,
                 RegistrationFSM,
                 MenuFSM)
from keyboards import (reg_profile_keys,
                       yesno_keys,
                       sexf_keys,
                       sex_keys,
                       skip_keys,
                       menu_keys)
from vkapi import (vkuser_info,
                   find_city)
from validators import (valid_name,
                        valid_age,
                        valid_purpose,
                        valid_description)
from funcs import (gen_purposes,
                   gen_profile)
from dbase import (reg_profile)

reg_profile_router = DefaultRouter()