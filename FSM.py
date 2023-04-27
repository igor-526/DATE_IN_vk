from vkwave.bots.fsm import FiniteStateMachine, State

fsm = FiniteStateMachine()

class RegistrationFSM:
    registration = State('registration')
    reg_profile = State('reg_profile')
    reg_name_auto = State('reg_name_auto')
    reg_name = State('reg_name')
    reg_age_auto = State('reg_age_auto')
    reg_age = State('reg_age')
    reg_sex_f = State('reg_sex_f')
    reg_sex_auto = State('reg_sex_auto')
    reg_sex = State('reg_sex')
    reg_age_min = State('reg_age_min')
    reg_age_max = State('reg_age_max')
    reg_city_auto = State('reg_city_auto')
    reg_city = State('reg_city')
    reg_purpose = State('reg_purpose')
    reg_photo = State('reg_photo')
    reg_description = State('reg_description')


class Reg:
    profile = State('profile')
    name_auto = State('name')
    name_manual = State('name_manual')


class MenuFSM:
    menu = State('menu')


class ProfileFSM:
    show = State('show')
    delete = State('delete')