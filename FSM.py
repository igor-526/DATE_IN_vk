from vkwave.bots.fsm import FiniteStateMachine, State

fsm = FiniteStateMachine()


class Reg:
    profile = State('profile')
    name_auto = State('name')
    name_manual = State('name_manual')
    bdate_manual = State('bdate_manual')
    bdate_auto = State('bdate_auto')
    bdate_year = State('bdate_year')
    sex_manual = State('sex_manunal')
    geo = State('geo')
    photo = State('photo')
    description = State('description')
    purposes = State('purposes')
    f_sex = State('f_sex')
    f_age_min = State('f_min_age')
    f_age_max = State('f_max_age')


class MenuFSM:
    menu = State('menu')


class ProfileFSM:
    show = State('show')
    delete = State('delete')